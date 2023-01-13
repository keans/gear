import logging
from typing import Any, Union
from pathlib import Path

from gear.base.basefiletype import BaseFileType
from gear.base.baseplugin import BasePlugin
from gear.utils.typing import PathOrString
from gear.utils.utils import ensure_path


# prepare logger
log = logging.getLogger(__name__)


class ReaderPluginException(Exception):
    """
    base reader exception
    """


class ReaderPlugin(BasePlugin, BaseFileType):
    """
    reader plugin
    """
    GLOBS = [".*"]

    def __init__(self, schema: dict = {}, is_binary: bool = False):
        BasePlugin.__init__(self, schema)
        BaseFileType.__init__(self, {}, filename=None, is_binary=is_binary)

    @classmethod
    def match(
        cls,
        filename: Union[str, Path],
        regex: str = None
    ) -> bool:
        """
        returns True, when filename matches globs

        :param filename: filename
        :type filename: str or Path
        :param regex: regex to limit the matches
        :type regex: str
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
        plugins = BasePlugin.get_plugins(
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

        if not self.match(filename=self.filename, regex=None):
            # invalid filetype for reader plugin
            raise NotImplementedError(
                f"Unknown filename type '{self.filename.suffix}' "
                f"(valid type: {', '.join(ReaderPlugin.GLOBS)})!"
            )

        # open the file either as binary or as text
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

    def init(
        self,
        filename: PathOrString,
        config_name: str,
        **kwargs
    ):
        self.filename = filename
        self.set_config(
            config_name=config_name,
            value=kwargs
        )
