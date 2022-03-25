import hashlib
import json
from typing import Any

import luigi

from gear.utils.parameters import PathParameter
from gear.utils.config import OUTPUT_DIR, PLUGIN_DIR
from gear.plugins.extractorplugin import ExtractorPlugin


class BaseTaskException(Exception):
    """
    base task exception
    """


class BaseTask(luigi.Task):
    input_filename = PathParameter()
    config = luigi.parameter.DictParameter()
    output_suffix = luigi.Parameter(default=".json")
    plugin_section = luigi.parameter.Parameter(default=None)

    @property
    def plugin_class(self):
        if self.plugin_section == "extractors":
            return ExtractorPlugin

        else:
            # undefined plugin section
            raise NotImplementedError(
                f"No plugin class defined for plugin section "
                f"'{self.plugin_section}'!"
            )

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
        h = hashlib.sha256(
            self.input_filename.as_posix().encode("utf-8")
        ).hexdigest()

        return f"{self.__class__.__name__}_{h}{self.output_suffix}"

    def output(self) -> Any:
        """
        returns the luigi output file as local target

        :return: luigi output file as local target
        :rtype: Any
        """
        return luigi.LocalTarget(
            OUTPUT_DIR.joinpath(self.output_filename)
        )

    def dump(self, value: dict):
        """
        dump given dictionary to

        :param value: dictionary with values to be stored
        :type value: dict
        """
        with self.output().open("w") as f:
            json.dump(value, f)

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
    def plugins(self) -> list:
        """
        returns all configured plugin class instances

        :return: returns all configured plugin class instances
        :rtype: list
        """
        plugins = []
        for config in self.config.get(self.plugin_section, []):
            for plugin_name in config:
                if plugin_name not in self.available_plugin_classes:
                    # unknown extractor plugin in config, but not installed
                    raise BaseTaskException(
                        f"Unknown plugin '{plugin_name}'!"
                    )

                # create extractor plugin instance
                plugins.append(
                    self.available_plugin_classes[plugin_name]()
                )

                 # initialize plugin with given config
                plugins[-1].init(
                    **(config or {}).get("kwargs", {})
                )

        return plugins

    #def requires(self):
    #    return []

