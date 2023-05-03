from pathlib import Path
from typing import Any

import luigi

from gear.utils.customtyping import PathOrString
from gear.utils.config import OUTPUT_DIR, PLUGIN_DIR
from gear.base.basetask import BaseTask
from gear.tasks.transformertask import TransformerTask
from gear.tasks.taskexceptions import ReporterTaskException


class ReportTask(BaseTask):
    """
    Task that is used to create a report of the transformed data.
    Corresponding report plugins will be used.
    """
    plugin_section = luigi.Parameter(default="reporters")

    def run(self):
        """
        run the report task
        """
        # apply plugins
        res = self.apply_plugins(
            data_generator=self.load()
        )

        # dump plugin results
        self.dump(res)

    def requires(self):
        """
        returns the list of required transformer tasks

        :return: list of required transformer tasks
        :rtype: list
        """
        return [
            TransformerTask(
                input_filename=self.input_filename,
                config=self.config,
                config_name=self.config_name
            )
        ]
