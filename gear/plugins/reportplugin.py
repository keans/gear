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

    def apply(
        self,
        header: dict,
        payload: dict
    ):
        """
        render given header and paylaod in template provided via configuration

        :param header: header information
        :type header: dict
        :param payload: payload information
        :type payload: dict
        """
        self._res[self.argconfig["template"]] = self.render(
            template_filename=self.argconfig["template"],
            header=header,
            payload=payload
        )

    def init(
        self,
        config_name: str,
        template_dir: PathOrString,
        **kwargs
    ):
        self.set_config(config_name=config_name, value=kwargs)
        self.template_dir = template_dir
