import logging
from abc import abstractmethod

from powerstrip import Plugin, PluginManager

from gear.base.argconfig.argconfig import ArgConfig


class PluginBase(Plugin):
    def __init__(self, schema):
        Plugin.__init__(self)

        self.log = logging.getLogger(__name__)
        self.schema = schema

    def set_config(self, value: dict):
        # set config
        self.argconfig = ArgConfig(schema=self.schema, d=value)

    @staticmethod
    def get_plugins(subclass, plugin_directory, tag) -> list:
        pm = PluginManager(plugin_directory, use_category=True)
        pm.discover()

        # get all plugin classes of the EvaluatorPlugin
        plugin_classes = pm.get_plugin_classes(
            subclass=subclass, tag=tag
        )

        return plugin_classes
