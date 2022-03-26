
from gear.base.pluginbase import PluginBase


class TransformerPlugin(PluginBase):
    """
    transformer plugin
    """
    def __init__(self, schema):
        PluginBase.__init__(self, schema)

        self._res = {}

    def init(self, **kwargs):
        self.set_config(kwargs)

    def run(self, fn):
        print("WORKING ON ")

    def shutdown(self):
        pass
