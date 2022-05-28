from pathlib import Path

from gear.base.pluginbase import PluginBase
from gear.base.mixins.templatemixin import TemplateMixin


# default report plugin schema
default_report_plugin_schema = {
    "template": {
        "type": "string"
    },
    "requires": {
        "type": "string"
    }
}


class ReporterPlugin(TemplateMixin, PluginBase):
    """
    report plugin
    """
    def __init__(self, schema=default_report_plugin_schema):
        PluginBase.__init__(self, schema)
        TemplateMixin.__init__(self)

        self._res = {}

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
