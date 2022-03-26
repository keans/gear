from pathlib import Path

from gear.base.pluginbase import PluginBase
from gear.utils.typing import PathOrString
from gear.utils.config import TEMPLATE_DIR
from gear.utils.render import render


# default report plugin schema
default_report_plugin_schema = {
    "template": {
        "type": "string"
    },
    "requires": {
        "type": "string"
    }
}


class ReporterPlugin(PluginBase):
    """
    report plugin
    """
    def __init__(self, schema=default_report_plugin_schema):
        PluginBase.__init__(self, schema)

        self._res = {}

    def render(self, template_filename: PathOrString, **kwargs) -> str:
        """
        render template file with given arguments

        :param template_filename: template filename
        :type template_filename: PathOrString
        :return: rendered template
        :rtype: str
        """
        return render(
            search_path=TEMPLATE_DIR.joinpath(self.__class__.__name__),
            template_filename=self.argconfig["template"],
            **kwargs
        )

    def apply(self, value: dict):
        """
        render given value in template provided via configuration

        :param value: arguments that should be rendered to the report
        :type value: dict
        """
        self._res[self.argconfig["template"]] = self.render(
            template_filename=self.argconfig["template"],
            **value
        )

    def init(self, **kwargs):
        self.set_config(kwargs)

    def run(self, fn):
        print("WORKING ON ")

    def shutdown(self):
        pass
