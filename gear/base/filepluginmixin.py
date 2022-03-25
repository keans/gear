import hashlib
import json
from pathlib import Path
from typing import Union, Any

import luigi

from gear.utils.config import OUTPUT_DIR


class FilePluginMixinException(Exception):
    """
    file plugin mixin exception
    """


class FilePluginMixin:
    """
    mixing class to extend luigin task class
    """
    def __init__(
        self,
        input_filename: Union[str, Path],
        suffix: str = ".status"
    ):
        self.input_filename = input_filename
        self.suffix = suffix

    @property
    def input_filename(self) -> Path:
        """
        returns the input filename

        :return: input filename
        :rtype: Path
        """
        return self._input_filename

    @input_filename.setter
    def input_filename(self, value: Union[str, Path]):
        """
        sets the input filename

        :param value: input filename
        :type value: Union[str, Path]
        """
        self._input_filename = (
            value
            if isinstance(value, Path) else
            Path(value)
        )

    @property
    def filetype(self) -> str:
        """
        returns the filetype of the input filename (without leading '.')

        :return: filetype of the input filename (without leading '.')
        :rtype: str
        """
        return Path(self.input_filename).suffix[1:]

    @property
    def suffix(self) -> str:
        """
        returns the suffix of the output file

        :return: suffix of the output file
        :rtype: str
        """
        return self._suffix

    @suffix.setter
    def suffix(self, value: str):
        """
        sets the suffix of the output filename (must start with '.')

        :param value: suffix of the output filename
        :type value: str
        """
        if not value.startswith("."):
            # invalid suffix
            FilePluginMixinException(
                f"The suffix must start with '.'!"
            )

        self._suffix = value

    @property
    def output_filename(self) -> str:
        """
        returns output filename as string consisting of the class name,
        the hexdigest of the input filename and the suffix

        :return: output filename
        :rtype: str
        """
        h = hashlib.sha256(
            self.input_filename.as_posix().encode("utf-8")
        ).hexdigest()

        return f"{self.__class__.__name__}_{h}{self.suffix}"

    def dump(self, value: dict):
        with self.output().open("w") as f:
            json.dump(value, f)
