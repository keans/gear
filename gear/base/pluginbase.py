import logging
from pathlib import Path
from abc import abstractmethod
from typing import Any

from powerstrip import Plugin, PluginManager

from gear.base.argconfig.argconfig import ArgConfig


class PluginBase(Plugin):
    """
    plugin base from which all plugins must be derived
    """
    def __init__(self, schema):
        Plugin.__init__(self)

        self.log = logging.getLogger(__name__)
        self.schema = schema

    def set_config(self, value: dict):
        """
        set the plugin's configuration

        :param value: configuration dictionary
        :type value: dict
        """
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
