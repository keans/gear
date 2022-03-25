import logging

from typing import Union, Generator
from pathlib import Path

from gear.utils.utils import ensure_path


# prepare logger
log = logging.getLogger(__name__)


class FileWalker:
    """
    walk through file directory
    """
    def __init__(
        self,
        directory: Union[str, Path],
        globs: list = ".*"
    ):
        self.directory = directory
        self.globs = globs

    @property
    def directory(self) -> Path:
        """
        returns the directory

        :return: directory
        :rtype: Path
        """
        return self._path

    @directory.setter
    def directory(self, value: Union[str, Path]):
        """
        set directory

        :param value: directory
        :type value: Union[str, Path]
        """
        assert isinstance(value, (str, Path))

        self._path = ensure_path(value, must_exist_dir=True)

    @property
    def globs(self) -> list:
        """
        returns the globs as list

        :return: list of globs
        :rtype: list
        """
        return self._globs

    @globs.setter
    def globs(self, value: Union[str, list]):
        """
        set globs

        :param value: list of globs
        :type value: list
        """
        assert isinstance(value, (str, list))

        if isinstance(value, str):
            # split string by ','
            value = [
                item
                for item in map(str.strip, value.split(","))
                if item != ""
            ]

        self._globs = []
        for item in value:
            self._globs.append(item)

    def walk(self, recursive: bool = False) -> Generator:
        """
        walk through directory and return all files that are
        matching the globs; if recursive is True, also all
        subdirectories will be considered

        :param recursive: if True, recursively visit subdirectories,
                          defaults to False
        :type recursive: bool, optional
        :yield: generator of filenames found
        :rtype: Generator
        """
        for g in self.globs:
            glob = f"**/*{g}" if recursive is True else f"*{g}"
            log.debug(
                f"getting files from '{self.directory.joinpath(glob)}'..."
            )
            yield from self.directory.glob(glob)

    def __repr__(self) -> str:
        return (
            f"<FileWalker(directory='{self.directory}', "
            f"globs={self.globs})"
        )
