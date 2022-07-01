from pathlib import Path

from gear.utils.typing import PathOrString
from gear.utils.utils import ensure_path


class DirectoryManager:
    """
    class to manage the directories of the output directory
    """
    def __init__(
        self,
        output_directory: PathOrString,
        config_directory: PathOrString,
        config_name: str
    ):
        self.config_name = config_name
        self.config_directory = config_directory
        self.output_directory = output_directory

    @property
    def config_directory(self) -> Path:
        """
        returns the config directory

        :return: config directory
        :rtype: Path
        """
        return self._config_directory

    @config_directory.setter
    def config_directory(self, value: PathOrString):
        """
        set the config directory

        :param value: config directory
        :type value: PathOrString
        """
        self._config_directory = ensure_path(
            path=value.joinpath(self.config_name),
            must_exist=True
        )

    @property
    def output_directory(self) -> Path:
        """
        returns the output directory

        :return: output directory
        :rtype: Path
        """
        return self._output_directory

    @output_directory.setter
    def output_directory(self, value: PathOrString):
        """
        set the output directory

        :param value: output directory
        :type value: PathOrString
        """
        self._output_directory = ensure_path(
            path=value.joinpath(self.config_name),
            create_dir=True
        )

    @property
    def templates_directory(self):
        return self.config_directory.joinpath("templates/")

    @property
    def temp_directory(self):
        return self.output_directory.joinpath("tmp/")

    @property
    def report_directory(self):
        return self.output_directory.joinpath("report/")

    @property
    def report_theme_directory(self):
        return self.report_directory.joinpath("theme/")
