from abc import ABC
from pathlib import Path
from typing import Union

from gear.utils.utils import ensure_path


class BaseFileType(ABC):
    def __init__(self, filename):
        self.filename = filename

    @property
    def filename(self) -> Path:
        """
        returns the filename

        :return: filename
        :rtype: Path
        """
        return self._filename

    @filename.setter
    def filename(self, value: Union[str, Path]):
        """
        set filename

        :param value: filename
        :type value: Union[str, Path]
        """
        self._filename = ensure_path(value)
