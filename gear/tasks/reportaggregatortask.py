import luigi

from gear.utils.typing import PathOrString
from gear.tasks.reporttask import ReportTask
from gear.base.basetask import BaseTask
from gear.tasks.taskexceptions import ReportAggregatorTaskException


class ReportAggregatorTask(BaseTask):
    """
    Task that is used to create an aggregated report of the subreports.
    Corresponding report aggregation plugins will be used.
    """
    plugin_section = luigi.Parameter(default="reportaggregators")

    def run(self):
        """
        run the report aggregator task
        """
        # copy template
        for plugin in self.plugins:
            plugin.copy_template()

        # apply plugins
        res = self.apply_plugins(self.load())

        # write finally aggregated plugin results
        for plugin in self.plugins:
            plugin.write()

        # dump plugin results
        self.dump({"status": "done"})

    def requires(self):
        """
        returns the list of required report tasks

        :return: list of required report tasks
        :rtype: list
        """
        return [
            ReportTask(
                input_filename=self.input_filename,
                config=self.config,
                config_name=self.config_name
            )
        ]
