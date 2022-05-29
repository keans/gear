from pathlib import Path

from gear.utils.typing import PathOrString
from gear.utils.utils import ensure_path


class DirectoryManager:
    """
    class to manage the directories of the output directory
    """
    def __init__(self, base_directory: PathOrString, config_name: str):
        self.config_name = config_name
        self.base_directory = base_directory

    @property
    def base_directory(self) -> Path:
        """
        returns the base directory

        :return: base directory
        :rtype: Path
        """
        return self._base_directory

    @base_directory.setter
    def base_directory(self, value: PathOrString):
        """
        set the base directory

        :param value: base directory
        :type value: PathOrString
        """
        self._base_directory = ensure_path(
            value.joinpath(self.config_name), create_dir=True
        )

    @property
    def temp_directory(self):
        return self.base_directory.joinpath("tmp/")

    @property
    def templates_directory(self):
        return self.base_directory.joinpath("templates/")

    @property
    def report_directory(self):
        return self.base_directory.joinpath("report/")

    @property
    def report_theme_directory(self):
        return self.report_directory.joinpath("theme/")
