
from gear.base.pluginbase import PluginBase


class ExtractorPlugin(PluginBase):
    def __init__(self, schema):
        PluginBase.__init__(self, schema)

        self._res = {}

    @staticmethod
    def get_plugins(plugin_directory, tag):
        return PluginBase.get_plugins(
            subclass=ExtractorPlugin,
            plugin_directory=plugin_directory,
            tag=tag
        )

    def init(self, **kwargs):
        self.set_config(kwargs)

    def run(self, fn):
        print("WORKING ON ")

    def shutdown(self):
        pass
