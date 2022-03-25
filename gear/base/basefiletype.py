import abc
from pathlib import Path
from typing import Union

from gear.base.argconfig.argconfig import ArgConfig
from gear.utils.utils import ensure_path


class BaseFileTypeException(Exception):
    """
    base file type exception
    """


class BaseFileType(abc.ABC):
    """
    base file type
    """
    def __init__(
        self,
        argconfig_schema: dict,
        filename: Union[str, Path] = None,
        is_binary: bool = False,
        **kwargs
    ):
        self.filename = filename
        self.is_binary = is_binary
        self._f = None

        # prepare argument configuration validator
        self.argconfig = ArgConfig(argconfig_schema, kwargs)

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
        assert (value is None) or isinstance(value, (str, Path))

        if value is None:
            # filename not provided
            self._filename = None

        else:
            # ensure that value is a Path
            self._filename = ensure_path(value)

    def ensure_filename_set(self, must_exist: bool = False):
        """
        if filename is not set and exception is raised

        :param must_exist: if True, filename must exist otherwise exception
                           is raised
        :raises BaseFileTypeException: filename not set exception
        """
        if self.filename is None:
            raise BaseFileTypeException(
                "The filename is not set!"
            )

        if (must_exist is True) and (not self.filename.exists()):
            # filename does not exist
            raise BaseFileTypeException(
                f"The filename '{self.filename}' does not exist!"
            )

    def ensure_file_is_opened(self):
        """
        ensure that the file is opened

        :raises BaseReaderException: exception that the file is not opened
        """
        if self._f is None:
            # file is not opened
            raise BaseFileTypeException(
                "The file is not opened!"
            )

    def __repr__(self) -> str:
        """
        returns the string representation of the file reader

        :return: string representation of the file reader
        :rtype: str
        """
        return (
            f"<{self.__class__.__name__}(filename={self.filename})"
        )
