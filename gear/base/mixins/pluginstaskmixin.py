from email.generator import Generator
from typing import Any

import luigi

from gear.base.exceptions import PluginsTaskMixinException
from gear.plugins.extractorplugin import ExtractorPlugin
from gear.plugins.transformerplugin import TransformerPlugin
from gear.plugins.reporterplugin import ReporterPlugin
from gear.plugins.reportaggregatorplugin import ReportAggregatorPlugin


class PluginsTaskMixin:
    """
    plugins task mixin that can be used as partial subclass
    for tasks
    """

    @property
    def plugin_class(self) -> Any:
        """
        get all plugin classes based on internal plugin_section variable

        :raises NotImplementedError: raised, if no plugin class found
        :return: plugin class
        :rtype: Any
        """
        # get plugin class based on plugin section
        plugin_cls = {
            "extractors": ExtractorPlugin,
            "transformers": TransformerPlugin,
            "reporters": ReporterPlugin,
            "reportaggregators": ReportAggregatorPlugin
        }.get(self.plugin_section, None)

        if plugin_cls is None:
            # undefined plugin section
            raise NotImplementedError(
                f"No plugin class defined for plugin section "
                f"'{self.plugin_section}'!"
            )

        return plugin_cls

    @property
    def plugins(self) -> list:
        """
        returns all configured plugin class instances

        :return: returns all configured plugin class instances
        :rtype: list
        """
        if getattr(self, "_plugins", None) is None:
            # plugins not yet initialized => initialize now
            self._plugins = []
            for config in self.config.get(self.plugin_section, []):
                for plugin_name, plugin_config in config.items():
                    if plugin_name not in self.available_plugin_classes:
                        # unknown plugin in config, but not installed
                        raise PluginsTaskMixinException(
                            f"Unknown plugin '{plugin_name}'!"
                        )

                    # create extractor plugin instance
                    self._plugins.append(
                        self.available_plugin_classes[plugin_name]()
                    )

                    # initialize plugin with given config
                    self._plugins[-1].init(
                        config_name=self.config_name,
                        **(plugin_config or {}).get("kwargs", {})
                    )

        return self._plugins

    def apply_plugins(self, data_generator: Generator) -> dict:
        """
        load data and apply the plugins on it

        :raises PluginsTaskMixinException: raised, if required plugin
                                           is missing
        :return: dictionary of plugin results
        :rtype: dict
        """
        for data in data_generator:
            # get payload from data generator
            payload = data.get("payload", {})
            for plugin in self.plugins:
                # get required plugins
                required_plugins = set(
                    map(str.strip, plugin.argconfig["requires"].split(","))
                )

                # check for missing ones that are required as input
                missing_plugins = (
                    required_plugins - set(payload.keys())
                )
                if len(missing_plugins) > 0:
                    # missing plugin input
                    raise PluginsTaskMixinException(
                        f"The plugin '{plugin.metadata.name}' "
                        f"requires the following plugins: "
                        f"{', '.join(missing_plugins)}"
                    )

                # apply to input data
                plugin.apply(
                    value={
                        required_plugin: payload[required_plugin]
                        for required_plugin in required_plugins
                    }
                )

        # collect overall result from plugins' results
        return {
            plugin.metadata.name: plugin._res
            for plugin in self.plugins
        }
