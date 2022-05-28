from pathlib import Path

from gear.utils.typing import PathOrString
from gear.utils.render import render


class TemplateMixin:
    """
    template mixin that can be used for classes that should use
    template rendering
    """
    @property
    def template_dir(self) -> Path:
        """
        returns the template directory of the report plugin consisting of
        base template directory and the reporter plugin's class name

        :return: template directory
        :rtype: Path
        """
        return self.directory.joinpath(self.__class__.__name__)

    @property
    def template_filename(self) -> Path:
        """
        returns the template filename within the template directory

        :return: template filename
        :rtype: Path
        """
        return self.template_dir.joinpath(self.argconfig["template"])

    def init_template(self, kwargs: dict):
        """
        initialize the template directory and add empty
        template if not existing

        :param kwargs: dictionary with values that should be rendered
        """
        if self.template_filename.exists():
            # do nothing if template does already exist
            return

        # template file does not exist yet
        self.log.debug(
            f"Creating empty template file '{self.template_filename}'..."
        )

        # ensure that template directory is existing
        self.template_dir.mkdir(parents=True, exist_ok=True)

        # create empty file
        with self.template_filename.open("w") as f:
            f.write(
                f"Add your template's content to "
                f"'{self.template_filename}'\n{kwargs}"
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
        self.init_template(kwargs)

        return render(
            search_path=self.template_dir,
            template_filename=self.argconfig["template"],
            **kwargs
        )
