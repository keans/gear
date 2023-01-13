import shutil
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
        schema: dict = default_report_plugin_schema
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
        self._res[self.template_filename_without_path] = self.render(
            template_filename=self.template_filename_without_path,
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
        self.template_dir = template_dir.joinpath(
            f"{self.__class__.__name__}"
        )

        if not self.template_dir.is_dir():
            # template directory of configuration for plugin
            # is not existing yet => copy default from plugin
            self.template_dir.mkdir()

            # get data directory from plugin directory
            data_dir = self.directory.joinpath("data/")

            if not data_dir.exists():
                # original data directory does not exist
                self.log.warning(
                    f"The directory '{data_dir}' does not exist! Skipping "
                    f"copying of data files from plugin."
                )

            else:
                # copy data from data directory to config template directory
                self.log.info(
                    f"Copying data from '{data_dir}' to "
                    f"'{self.template_dir}'..."
                )
                shutil.copytree(
                    src=data_dir,
                    dst=self.template_dir
                )
