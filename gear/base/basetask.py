import datetime
import hashlib
import json
from pathlib import Path
from typing import Any, Generator
from gear.base.mixins.templatemixin import TemplateMixin

import luigi


from gear.utils.parameters import PathParameter
from gear.utils.directorymanager import DirectoryManager
from gear.utils.taskdumper import TaskDumper
from gear.utils.config import OUTPUT_DIR, CONFIG_DIR, PLUGIN_DIR
from gear.base.exceptions import BaseTaskException
from gear.plugins.extractorplugin import ExtractorPlugin
from gear.plugins.transformerplugin import TransformerPlugin
from gear.plugins.reportplugin import ReportPlugin
from gear.plugins.reportaggregatorplugin import ReportAggregatorPlugin


class BaseTask(luigi.Task):
    """
    base task class that is used as parent for all other tasks
    """
    input_filename = PathParameter()
    config = luigi.parameter.DictParameter()
    config_name = luigi.Parameter()
    plugin_section = luigi.Parameter()
    output_suffix = luigi.Parameter(default=".json")

    @property
    def filetype(self) -> str:
        """
        returns the filetype of the input filename (without leading '.')

        :return: filetype of the input filename (without leading '.')
        :rtype: str
        """
        return self.input_filename.suffix[1:]

    @property
    def output_dir(self) -> Path:
        """
        returns the output directory

        :return: output directrory
        :rtype: Path
        """
        return self.directory_manager.temp_directory

    @property
    def output_filename(self) -> str:
        """
        returns output filename as string consisting of the class name,
        the hexdigest of the input filename and the suffix

        :return: output filename
        :rtype: str
        """
        # compute hash of input filename
        h = hashlib.sha256(
            self.input_filename.as_posix().encode("utf-8")
        ).hexdigest()

        return self.output_dir.joinpath(
            f"{self.__class__.__name__}_{h}{self.output_suffix}"
        )

    @property
    def available_plugin_classes(self) -> list:
        """
        returns all available plugin classes

        :return: returns all available plugin classes
        :rtype: list
        """
        return self.plugin_class.get_plugins(
            plugin_directory=PLUGIN_DIR,
            tag=self.filetype
        ).get(self.plugin_section, {})

    @property
    def directory_manager(self) -> DirectoryManager:
        """
        returns an instance of the directory manager that is
        used to manage the directories

        :return: directory manager
        :rtype: DirectoryManager
        """
        return DirectoryManager(
            output_directory=OUTPUT_DIR,
            config_directory=CONFIG_DIR,
            config_name=self.config_name
        )

    def output(self) -> Any:
        """
        returns the luigi output file as local target

        :return: luigi output file as local target
        :rtype: Any
        """
        return luigi.LocalTarget(self.output_filename)

    def load(self) -> Generator:
        """
        load input files and return their content as generator

        :yield: file input
        :rtype: Generator
        """
        for input_file in self.input():
            with input_file.open("r") as f:
                yield TaskDumper.from_file(f=f)

    def dump(self, value: dict):
        """
        dump given dictionary to a file

        :param value: dictionary with values to be stored
        :type value: dict
        """
        with self.output().open("w") as f:
            # use task dumper to dump the dictionary information
            td = TaskDumper(
                input_filename=self.input_filename.as_posix(),
                payload=value
            )
            td.dump(f)

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
            "reporters": ReportPlugin,
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
                        raise BaseTaskException(
                            f"Unknown plugin '{plugin_name}'!"
                        )

                    # create extractor plugin instance
                    self._plugins.append(
                        self.available_plugin_classes[plugin_name]()
                    )

                    if not isinstance(self._plugins[-1], TemplateMixin):
                        # initialize plugin with given config
                        self._plugins[-1].init(
                            config_name=self.config_name,
                            **(plugin_config or {}).get("kwargs", {})
                        )

                    else:
                        # initialize special template based plugins
                        # with given config and template directory
                        self._plugins[-1].init(
                            config_name=self.config_name,
                            template_dir=(
                                self.directory_manager.templates_directory
                            ),
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
        for task_dumper in data_generator:
            # get payload from data generator
            for plugin in self.plugins:
                if not plugin.argconfig.contains("requires"):
                    # configuration of plugin is missing
                    raise BaseException(
                        f"The plugin '{plugin.metadata.name}' "
                        f"did not specify 'requires' in the 'kwargs' "
                        f"section of its configuration"
                    )

                # get required plugins
                required_plugins = set(
                    map(str.strip, plugin.argconfig["requires"].split(","))
                )

                # check for missing ones that are required as input
                missing_plugins = (
                    required_plugins - set(task_dumper.payload.keys())
                )
                if len(missing_plugins) > 0:
                    # missing plugin input
                    raise BaseTaskException(
                        f"The plugin '{plugin.metadata.name}' "
                        f"requires the following plugins: "
                        f"{', '.join(missing_plugins)}"
                    )

                # apply to input data
                plugin.apply(
                    header=task_dumper.header,
                    payload={
                        required_plugin: task_dumper.payload[required_plugin]
                        for required_plugin in required_plugins
                    }
                )

        # collect overall result from plugins' results
        return {
            plugin.metadata.name: plugin._res
            for plugin in self.plugins
        }
