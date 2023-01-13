import logging
from pathlib import Path

from gear.utils.typing import PathOrString
from gear.utils.render import render
from gear.utils.utils import ensure_path
from gear.base.exceptions import TemplateMixinException


# prepare logger
log = logging.getLogger(__name__)


class TemplateMixin:
    """
    template mixin that can be used for classes that should use
    template rendering
    """
    def __init__(self):
        self.template_dir = None

    @property
    def template_dir(self) -> Path:
        """
        return the template dir

        :return: template directory
        :rtype: Path
        """
        return self._template_dir

    @template_dir.setter
    def template_dir(self, value: PathOrString):
        """
        set the template directory

        :param value: template directory
        :type value: PathOrString
        """
        if value is None:
            self._template_dir = None
        else:
            self._template_dir = ensure_path(value)

    @property
    def template_filename_without_path(self) -> str:
        """
        returns the template filename without path, i.e., either
        the template name from the configuration (if set) or otherwise
        the classname is used as default

        :return: template filename without path
        :rtype: str
        """
        if self.argconfig.contains("template"):
            # template explicitly define in config
            return self.argconfig["template"]

        # if not set, use class name as default
        return f"{self.__class__.__name__}.html"

    @property
    def template_filename(self) -> Path:
        """
        returns the template filename within the template directory

        :return: template filename
        :rtype: Path
        """
        assert (self.template_dir is not None)

        return self.template_dir.joinpath(
            self.template_filename_without_path
        )

    def render(self, template_filename: PathOrString, **kwargs) -> str:
        """
        render template file with given arguments

        :param template_filename: template filename
        :type template_filename: PathOrString
        :return: rendered template
        :rtype: str
        """
        # initialize template
        if not self.template_filename.exists():
            raise TemplateMixinException(
                f"The template file '{self.template_filename}' does not exist!"
            )

        log.debug(
            f"rendering in '{self.template_dir}' the template "
            f"'{self.argconfig['template']}' with values {kwargs}..."
        )
        return render(
            search_path=self.template_dir,
            template_filename=self.template_filename_without_path,
            **kwargs
        )
