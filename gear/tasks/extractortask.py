from pathlib import Path
from typing import Any

import luigi

from gear.utils.typing import PathOrString
from gear.utils.config import OUTPUT_DIR, PLUGIN_DIR
from gear.base.basetask import BaseTask
from gear.plugins.readerplugin import ReaderPlugin


class ExtractorTask(BaseTask):
    """
    Task that is used for the extraction of wanted data.
    Corresponding reader plugins will be used depending on the input data
    """
    plugin_section = luigi.Parameter(default="extractors")

    def run(self):
        """
        run the extractor task
        """
        # get reader for the given filetype
        reader = ReaderPlugin.get_plugin(
            plugin_directory=PLUGIN_DIR,
            tag=self.filetype
        )()

        # initialize the reader
        reader.init(
            filename=self.input_filename,
            config_name=self.config_name,
            **(self.config or {}).get("kwargs", {})
        )

        # use reader to read input file row-wise
        with reader as r:
            for no, row in enumerate(r):
                # apply all extractor plugins
                for plugin in self.plugins:
                    plugin.apply(no, row)

        # collect overall result from plugins' results
        res = {
            plugin.metadata.name: plugin._res
            for plugin in self.plugins
        }

        # dump plugin results
        self.dump(res)
