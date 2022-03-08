import logging
from typing import Any

from gear.filetypes.base.basefiletype import BaseFileType


# prepare logger
log = logging.getLogger(__name__)


class BaseReaderException(Exception):
    """
    base reader exception
    """


class BaseReader(BaseFileType):
    """
    base reader
    """
    def __enter__(self):
        """
        enter context manager
        """
        # ensure that filename is set for loading and that it does exist
        self.ensure_filename_set(must_exist=True)

        self._f = self.filename.open("rb" if self.is_binary else "r")

        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any):
        """
        exit context manager

        :param exc_type: executable type
        :type exc_type: Any
        :param exc_value: executable value
        :type exc_value: Any
        :param traceback: traceback
        :type traceback: Any
        """
        self._f.close()

    def __iter__(self):
        """
        iterate over file reader

        :return: iteratable generator
        :rtype: Generator
        """
        if self._f is None:
            # file not opened
            raise BaseReaderException(
                "File must be opened first."
            )

        return (row for row in self._f)
