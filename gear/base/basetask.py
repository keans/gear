from email.generator import Generator
import hashlib
import json
from typing import Any

import luigi

from gear.utils.parameters import PathParameter
from gear.utils.config import OUTPUT_DIR, PLUGIN_DIR
from gear.plugins.extractorplugin import ExtractorPlugin
from gear.plugins.transformerplugin import TransformerPlugin
from gear.plugins.reporterplugin import ReporterPlugin


class BaseTaskException(Exception):
    """
    base task exception
    """


class BaseTask(luigi.Task):
    """
    base task
    """
    input_filename = PathParameter()
    config = luigi.parameter.DictParameter()
    output_suffix = luigi.Parameter(default=".json")
    plugin_section = luigi.parameter.Parameter(default=None)

    @property
    def plugin_class(self) -> Any:
        """
        get all plugin classes based on internal plugin_section variable

        :raises NotImplementedError: raised, if no plugin class found
        :return: plugin class
        :rtype: Any
        """
        # get plugin class based on plugin section
        plugin_cls = {
            "extractors": ExtractorPlugin,
            "transformers": TransformerPlugin,
            "reporters": ReporterPlugin
        }.get(self.plugin_section, None)

        if plugin_cls is None:
            # undefined plugin section
            raise NotImplementedError(
                f"No plugin class defined for plugin section "
                f"'{self.plugin_section}'!"
            )

        return plugin_cls

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
            for plugin_name, plugin_config in config.items():
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
                    **(plugin_config or {}).get("kwargs", {})
                )

        return plugins

    def output(self) -> Any:
        """
        returns the luigi output file as local target

        :return: luigi output file as local target
        :rtype: Any
        """
        return luigi.LocalTarget(
            OUTPUT_DIR.joinpath(self.output_filename)
        )

    def load(self) -> Generator:
        """
        load input files

        :yield: file input
        :rtype: Generator
        """
        for input_file in self.input():
            with input_file.open("r") as f:
                yield json.load(f)

    def dump(self, value: dict):
        """
        dump given dictionary to

        :param value: dictionary with values to be stored
        :type value: dict
        """
        with self.output().open("w") as f:
            json.dump(value, f)
