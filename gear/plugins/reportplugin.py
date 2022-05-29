from pathlib import Path

from gear.base.baseplugin import BasePlugin
from gear.base.mixins.templatemixin import TemplateMixin
from gear.utils.typing import PathOrString


# default report plugin schema
default_report_plugin_schema = {
    "template": {
        "type": "string"
    },
    "requires": {
        "type": "string"
    }
}


class ReportPlugin(TemplateMixin, BasePlugin):
    """
    report plugin
    """
    def __init__(
        self,
        schema=default_report_plugin_schema
    ):
        BasePlugin.__init__(self, schema)
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
        template_dir: PathOrString,
        **kwargs
    ):
        self.set_config(config_name=config_name, value=kwargs)
        self.template_dir = template_dir
