import luigi

from gear.utils.config import PLUGIN_DIR
from gear.utils.filewalker import FileWalker
from gear.tasks.reportaggregatortask import ReportAggregatorTask
from gear.plugins.readerplugin import ReaderPlugin
from gear.evaluator.base.evaluatorconfig.evaluatorconfig import \
    EvaluatorConfig


class StartTask(luigi.WrapperTask):
    """
    start task to initiate the overall process
    """
    # main configuration file
    config_filename = luigi.parameter.Parameter()
    # source directory from which data files will be read
    src_directory = luigi.parameter.Parameter()

    def _get_readers(self, evaluator_config: EvaluatorConfig) -> dict:
        """
        returns a dictionary of all installed readers with the
        filetype name as key and the corresponding plugin instance as value

        :param evaluator_config: evaluator config
        :type evaluator_config: EvaluatorConfig
        :return: dictionary of readers
        :rtype: dict
        """
        return {
            filetype_name: ReaderPlugin.get_plugin(
                plugin_directory=PLUGIN_DIR,
                tag=filetype["filetype"]
            )
            for filetype_name, filetype in evaluator_config.filetypes.items()
        }

    def requires(self):
        # load the configuration file
        evaluator_config = EvaluatorConfig.from_file(
            filename=self.config_filename
        )

        # create dict of all readers by filetype to have quick
        # access to the readers' regexes during file walk
        # (no need for correct init with parameters here)
        readers = self._get_readers(evaluator_config)

        # prepare target list for required sub tasks
        sub_tasks = []

        # prepare file walker for filetype
        fw = FileWalker(directory=self.src_directory)
        for filename in fw.walk(recursive=False):
            for filetype_name, filetype in evaluator_config.filetypes.items():
                # get config of filetype
                config = filetype.get("kwargs", {})

                # get reader for each filetype
                reader = readers[filetype_name]
                if reader.match(
                    filename=filename,
                    regex=config.get("regex", None)
                ):
                    # reader is matching the file type
                    # => append reporter aggregator task
                    sub_tasks.append(
                        ReportAggregatorTask(
                            input_filename=filename,
                            config=filetype,
                            config_name=self.config_filename.stem
                        )
                    )

        return sub_tasks
