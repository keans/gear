
from gear.base.baseplugin import BasePlugin
from gear.utils.typing import PathOrString


class ExtractorPlugin(BasePlugin):
    """
    extractor plugin
    """
    def __init__(self, schema: dict = {}):
        BasePlugin.__init__(self, schema)
        self._res = {}
