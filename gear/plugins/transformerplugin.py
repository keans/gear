
from gear.base.baseplugin import BasePlugin


class TransformerPlugin(BasePlugin):
    """
    transformer plugin
    """
    def __init__(self, schema):
        BasePlugin.__init__(self, schema)

        self._res = {}
