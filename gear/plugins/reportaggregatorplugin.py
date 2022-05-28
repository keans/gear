import shutil
from pathlib import Path
import inspect

import luigi

from gear.tasks.taskexceptions import ReportAggregatorTaskException
from gear.base.pluginbase import PluginBase
from gear.base.mixins.templatemixin import TemplateMixin
from gear.utils.typing import PathOrString
from gear.utils.config import OUTPUT_DIR
from gear.utils.render import render


# default report aggregator plugin schema
default_report_aggregator_plugin_schema = {
    "template": {
        "type": "string"
    },
    "theme": {
        "type": "string"
    },
    "requires": {
        "type": "string"
    }
}


class ReportAggregatorPlugin(TemplateMixin, PluginBase):
    """
    reporter aggregator plugin
    """
    def __init__(self, schema=default_report_aggregator_plugin_schema):
        PluginBase.__init__(self, schema)
        TemplateMixin.__init__(self)

        self._res = {}

    @property
    def theme_path(self) -> Path:
        """
        returns the Path of where the theme is located

        :raises ReportAggregatorTaskException: if theme path does not exist,
                                               exception is raised
        :return: Path where theme is located
        :rtype: Path
        """
        # get theme path
        theme_path = self.directory.joinpath(
            "themes", self.argconfig["theme"]
        )
        if not theme_path.is_dir():
            # source theme path directory is not existing
            raise ReportAggregatorTaskException(
                f"The theme directory '{theme_path}' does not exist!"
            )

        return theme_path

    def copy_template(self):
        """
        copy the template directory to the output directory
        """
        theme_output_dir = OUTPUT_DIR.joinpath(
            self.config_name,
            self.argconfig["theme"]
        )

        if not theme_output_dir.exists():
            # copy theme to output directory, if not existing
            shutil.copytree(self.theme_path, theme_output_dir)

            # remove base.html from target path since rendering
            # will not take place in the output path, but before
            Path(theme_output_dir, "base.html").unlink()

    def apply(self, value: dict):
        """
        render given value in template provided via configuration

        :param value: arguments that should be rendered to the report
        :type value: dict
        """
        self._res[self.argconfig["template"]] = self.render(
            template_filename=self.argconfig["template"],
            theme_path=self.theme_path,
            **value
        )

    def write(self):
        for template_name, content in self._res.items():
            with open(OUTPUT_DIR.joinpath(template_name), "w") as f:
                f.write(content)

    def init(
        self,
        config_name: str,
        **kwargs
    ):
        self.set_config(config_name=config_name, value=kwargs)

    def run(self, fn):
        print("WORKING ON ")

    def shutdown(self):
        pass
