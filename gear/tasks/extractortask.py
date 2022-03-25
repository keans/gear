from pathlib import Path
from typing import Any

import luigi
from luigi.util import requires

from gear.utils.config import OUTPUT_DIR, PLUGIN_DIR
from gear.base.filepluginmixin import FilePluginMixin
from gear.base.basetask import BaseTask
from gear.plugins.extractorplugin import ExtractorPlugin
from gear.plugins.readerplugin import ReaderPlugin


class ExtractorTaskException(Exception):
    """
    extractor task exception
    """


class ExtractorTask(BaseTask):
    def __init__(self, input_filename, config, *args, **kwargs):
        BaseTask.__init__(
             self,
             input_filename=input_filename,
             config=config,
             plugin_section="extractors",
        )

    def run(self):
        # get plugins
        plugins = self.plugins

        # get reader for filetype and create initalize it
        reader = ReaderPlugin.get_plugin(
            plugin_directory=PLUGIN_DIR,
            tag=self.filetype
        )()
        reader.init(
            filename=self.input_filename,
            config=(self.config or {}).get("kwargs", {})
        )

        # use reader to read input file row-wise
        with reader as r:
            for no, row in enumerate(r):
                # apply all extractor plugins
                for plugin in plugins:
                    plugin.apply(no, row)

        res = {}
        for plugin in plugins:
            name = plugin.metadata.name

            i = 0
            while True:
                if name not in res:
                    break
                i += 1
                name = f"{plugin.metadata.name}_{i}"

            res[name] = plugin._res

        # dump plugin results
        self.dump(res)

        #     # plugin lifecycle
        #     extractor_plugin.init()
        #     extractor_plugin.run(fn)
        #     extractor_plugin.shutdown()
