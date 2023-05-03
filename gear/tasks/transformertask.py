from pathlib import Path
from typing import Any
from gear.tasks.taskexceptions import TransformerTaskException

import luigi

from gear.utils.customtyping import PathOrString
from gear.utils.config import OUTPUT_DIR, PLUGIN_DIR
from gear.base.basetask import BaseTask

from gear.tasks.extractortask import ExtractorTask


class TransformerTask(BaseTask):
    """
    Task that is used to transform the extracted data into another format.
    Corresponding transformer plugins will be used.
    """
    plugin_section = luigi.Parameter(default="transformers")

    def run(self):
        """
        run the transformer task
        """
        # apply plugins
        res = self.apply_plugins(self.load())

        # dump plugin results
        self.dump(res)

    def requires(self) -> list:
        """
        returns the list of required extractor tasks

        :return: list of required extractor tasks
        :rtype: list
        """
        return [
            ExtractorTask(
                input_filename=self.input_filename,
                config=self.config,
                config_name=self.config_name
            )
        ]
