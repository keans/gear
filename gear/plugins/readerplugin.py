import logging
from typing import Any, Union
from pathlib import Path

from gear.base.basefiletype import BaseFileType
from gear.base.pluginbase import PluginBase
from gear.utils.utils import ensure_path


# prepare logger
log = logging.getLogger(__name__)


class ReaderPluginException(Exception):
    """
    base reader exception
    """


class ReaderPlugin(PluginBase, BaseFileType):
    """
    reader plugin
    """
    GLOBS = [".*"]

    def __init__(self, schema):
        PluginBase.__init__(self, schema)
        BaseFileType.__init__(self, {}, filename=None)

    @classmethod
    def match(cls, filename: Union[str, Path], regex: str = None) -> bool:
        """
        returns True, when filename matches globs

        :param filename: filename
        :type filename: str or Path
        :return: True, if filename matches glob
        :rtype: bool
        """
        assert isinstance(cls.GLOBS, list)

        # ensure filename
        filename = ensure_path(filename)

        for glob in cls.GLOBS:
            if (
                filename.match(glob) and
                ((regex is None) or filename.match(regex))
            ):
                # filename matches the glob and the given regex
                return True

        return False

    @staticmethod
    def get_plugin(plugin_directory, tag):
        plugins = PluginBase.get_plugins(
            subclass=ReaderPlugin,
            plugin_directory=plugin_directory,
            tag=tag
        )

        if len(plugins["readers"]) == 0:
            # no reader plugin found
            raise ReaderPluginException(
                f"No ReaderPlugin found for '{tag}'!"
            )

        elif len(plugins["readers"]) > 1:
            # more than one plugin found
            raise ReaderPluginException(
                f"More than one ReaderPlugin found for '{tag}'!"
            )

        # return single reader plugin
        return next(iter(plugins["readers"].values()))

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
            raise ReaderPluginException(
                "File must be opened first."
            )

        return (row for row in self._f)

    def init(self, filename: Union[str, Path], config: dict):
        self.filename = filename

        self.set_config(config)

    def run(self, fn):
        print("WORKING ON ")

    def shutdown(self):
        pass
