import inspect
import logging
from pathlib import Path
from typing import Any
from gear.utils.typing import PathOrString

from powerstrip import Plugin, PluginManager

from gear.base.argconfig.argconfig import ArgConfig
from gear.utils.utils import ensure_path


class BasePlugin(Plugin):
    """
    base plugin from which all plugins must be derived
    """
    def __init__(self, schema: dict = {}):
        Plugin.__init__(self)

        self.log = logging.getLogger(__name__)
        self.schema = schema
        self.config_name = None

    @property
    def directory(self) -> Path:
        """
        returns the plugin's directory

        :return: plugin directory
        :rtype: Path
        """
        return Path(
            inspect.getfile(self.__class__)
        ).parent

    def set_config(
        self,
        config_name: str,
        value: dict
    ):
        """
        set the plugin's configuration

        :param config_name: name of the configuration
        :type config_name: str
        :param value: configuration dictionary
        :type value: dict
        """
        self.config_name = config_name
        self.argconfig = ArgConfig(schema=self.schema, d=value)

    @classmethod
    def get_plugins(
        cls,
        plugin_directory: Path,
        tag: str,
        subclass: Any = None
    ) -> list:
        """
        returns all plugins from plugin directory

        :param plugin_directory: plugin directory
        :type plugin_directory: Path
        :param tag: tag that is used for filtering all
        :type tag: str
        :param subclass: subclass used for filtering, if None current cls
        :type subclass: Any, optional
        :return: returns list of all plugins matching the filter
        :rtype: list
        """
        # discover all plugins in plugin directory
        pm = PluginManager(plugin_directory, use_category=True)
        pm.discover()

        # get all plugin classes of the EvaluatorPlugin
        return pm.get_plugin_classes(
            subclass=subclass or cls, tag=tag
        )

    def init(
        self,
        config_name: str,
        **kwargs
    ):
        self.set_config(
            config_name=config_name,
            value=kwargs
        )

    def run(self, fn):
        pass

    def shutdown(self):
        pass
