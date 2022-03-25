import luigi

from gear.utils.config import PLUGIN_DIR
from gear.evaluator.base.evaluatorconfig.evaluatorconfig import \
    EvaluatorConfig
from gear.tasks.extractortask import ExtractorTask
from gear.utils.filewalker import FileWalker
from gear.plugins.readerplugin import ReaderPlugin


class StartTask(luigi.WrapperTask):
    config_filename = luigi.parameter.Parameter()
    src_directory = luigi.parameter.Parameter()

    def requires(self):
        # load the configuration file
        ec = EvaluatorConfig.from_file(filename=self.config_filename)

        # create dict of all readers by filetype to
        # have quick access to the readers during file walk
        readers = {
            filetype["filetype"]: ReaderPlugin.get_plugin(
                plugin_directory=PLUGIN_DIR,
                tag=filetype["filetype"]
            )
            for filetype in ec.filetypes
        }

        # target list of required extractor tasks
        extractor_tasks = []

        # prepare file walker for filetype
        fw = FileWalker(directory=self.src_directory)
        for filename in fw.walk(recursive=False):
            for filetype in ec.filetypes:
                # get config of filetype
                config = filetype.get("kwargs", {})

                # get reader for each filetype
                reader = readers[filetype["filetype"]]
                if reader.match(
                    filename=filename,
                    regex=config.get("regex", None)
                ):
                    # reader is matching the file type
                    # => start extractor task
                    extractor_task = ExtractorTask(
                        input_filename=filename,
                        config=filetype
                    )
                    extractor_tasks.append(extractor_task)

        return extractor_tasks
