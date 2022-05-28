
from gear.base.pluginbase import PluginBase


class TransformerPlugin(PluginBase):
    """
    transformer plugin
    """
    def __init__(self, schema):
        PluginBase.__init__(self, schema)

        self._res = {}

    def init(
        self,
        config_name: str,
        **kwargs
    ):
        self.set_config(config_name=config_name, value=kwargs)

    def run(self, fn):
        print("WORKING ON ")

    def shutdown(self):
        pass
