import shutil
from pathlib import Path
import datetime
import getpass
from gear.utils.directorymanager import DirectoryManager

import luigi

from gear.tasks.taskexceptions import ReportAggregatorTaskException
from gear.base.baseplugin import BasePlugin
from gear.base.mixins.templatemixin import TemplateMixin
from gear.utils.typing import PathOrString
from gear.utils.config import OUTPUT_DIR, CONFIG_DIR
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


class ReportAggregatorPlugin(TemplateMixin, BasePlugin):
    """
    reporter aggregator plugin
    """
    def __init__(
        self,
        schema : dict = default_report_aggregator_plugin_schema
    ):
        BasePlugin.__init__(self, schema)
        TemplateMixin.__init__(self)

        self._res = {}

    @property
    def directory_manager(self) -> DirectoryManager:
        """
        return the instance of the directory manager

        :return: directory manager
        :rtype: DirectoryManager
        """
        return DirectoryManager(
            output_directory=OUTPUT_DIR,
            config_directory=CONFIG_DIR,
            config_name=self.config_name
        )

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
            "themes",
            self.argconfig["theme"]
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
        if not self.directory_manager.report_theme_directory.exists():
            # copy theme to output directory, if not existing
            shutil.copytree(
                self.theme_path,
                self.directory_manager.report_theme_directory
            )

            # move base.html to template directory
            try:
                shutil.move(
                    self.directory_manager.report_theme_directory.joinpath(
                        "base.html"
                    ),
                    self.directory_manager.templates_directory.as_posix()
                )
            except shutil.Error as e:
                # file exists already
                self.log.warning(e)

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
            payload=payload,
            created_at=datetime.datetime.now(),
            created_by=getpass.getuser()
        )

    def write(self):
        """
        write the plugins' content to the file
        """
        for template_name, content in self._res.items():
            # prepare output filename
            fn = self.directory_manager.report_directory.joinpath(
                template_name
            )

            # write content to the file
            with fn.open("w") as f:
                f.write(content)

    def init(
        self,
        config_name: str,
        template_dir: PathOrString,
        **kwargs
    ):
        self.set_config(config_name=config_name, value=kwargs)
        self.template_dir = template_dir
