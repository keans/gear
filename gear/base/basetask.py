import datetime
import hashlib
import json
from typing import Any, Generator

import luigi

from gear.base.mixins.pluginstaskmixin import PluginsTaskMixin
from gear.utils.parameters import PathParameter
from gear.utils.directorymanager import DirectoryManager
from gear.utils.config import OUTPUT_DIR, PLUGIN_DIR
from gear.utils.utils import get_user


class BaseTask(PluginsTaskMixin, luigi.Task):
    """
    base task class that is used as parent for all other tasks
    """
    input_filename = PathParameter()
    config = luigi.parameter.DictParameter()
    config_name = luigi.Parameter()
    plugin_section = luigi.Parameter()
    output_suffix = luigi.Parameter(default=".json")

    @property
    def filetype(self) -> str:
        """
        returns the filetype of the input filename (without leading '.')

        :return: filetype of the input filename (without leading '.')
        :rtype: str
        """
        return self.input_filename.suffix[1:]

    @property
    def output_filename(self) -> str:
        """
        returns output filename as string consisting of the class name,
        the hexdigest of the input filename and the suffix

        :return: output filename
        :rtype: str
        """
        # compute hash of input filename
        h = hashlib.sha256(
            self.input_filename.as_posix().encode("utf-8")
        ).hexdigest()

        return f"{self.__class__.__name__}_{h}{self.output_suffix}"

    @property
    def available_plugin_classes(self) -> list:
        """
        returns all available plugin classes

        :return: returns all available plugin classes
        :rtype: list
        """
        return self.plugin_class.get_plugins(
            plugin_directory=PLUGIN_DIR,
            tag=self.filetype
        ).get(self.plugin_section, {})

    @property
    def directory_manager(self) -> DirectoryManager:
        """
        returns an instance of the directory manager that is
        used to manage the directories

        :return: directory manager
        :rtype: DirectoryManager
        """
        return DirectoryManager(OUTPUT_DIR, self.config_name)

    def output(self) -> Any:
        """
        returns the luigi output file as local target

        :return: luigi output file as local target
        :rtype: Any
        """
        return luigi.LocalTarget(
            self.directory_manager.temp_directory.joinpath(
                self.output_filename
            )
        )

    def load(self) -> Generator:
        """
        load input files and return their content as generator

        :yield: file input
        :rtype: Generator
        """
        for input_file in self.input():
            with input_file.open("r") as f:
                yield json.load(f)

    def dump(self, value: dict):
        """
        dump given dictionary to

        :param value: dictionary with values to be stored
        :type value: dict
        """
        with self.output().open("w") as f:
            # prepare dictionary to be stored with header and payload
            d = {
                "header": {
                    "ts": datetime.datetime.now().isoformat(),
                    "input_filename": self.input_filename.as_posix(),
                    "user": get_user()
                },
                "payload": value,
            }

            # dump the dictionary
            json.dump(d, f)
