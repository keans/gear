import luigi

from gear.utils.config import PLUGIN_DIR
from gear.evaluator.base.evaluatorconfig.evaluatorconfig import \
    EvaluatorConfig
from gear.utils.filewalker import FileWalker
from gear.plugins.readerplugin import ReaderPlugin
from gear.tasks.extractortask import ExtractorTask
from gear.tasks.transformertask import TransformerTask
from gear.tasks.reportertask import ReporterTask


class StartTask(luigi.WrapperTask):
    config_filename = luigi.parameter.Parameter()
    src_directory = luigi.parameter.Parameter()

    def requires(self):
        # load the configuration file
        ec = EvaluatorConfig.from_file(filename=self.config_filename)

        # create dict of all readers by filetype to have quick
        # access to the readers' regexes during file walk
        # (no need for correct init with parameters here)
        readers = {
            filetype_name: ReaderPlugin.get_plugin(
                plugin_directory=PLUGIN_DIR,
                tag=filetype["filetype"]
            )
            for filetype_name, filetype in ec.filetypes.items()
        }

        # target list of required sub tasks
        sub_tasks = []

        # prepare file walker for filetype
        fw = FileWalker(directory=self.src_directory)
        for filename in fw.walk(recursive=False):
            for filetype_name, filetype in ec.filetypes.items():
                # get config of filetype
                config = filetype.get("kwargs", {})

                # get reader for each filetype
                reader = readers[filetype_name]
                if reader.match(
                    filename=filename,
                    regex=config.get("regex", None)
                ):
                    # reader is matching the file type
                    # => start extractor task
                    #task = ExtractorTask(
                    #task = TransformerTask(
                    task = ReporterTask(
                        input_filename=filename,
                        config=filetype
                    )
                    sub_tasks.append(task)

        return sub_tasks

    def run(self):
        import json
        for input_file in self.input():
            with input_file.open("r") as f:
                j = json.load(f)

                print("222222", j)
