from typing import Union
from pathlib import Path

from gear.utils.utils import ensure_path
from gear.evaluator.models.evaluatorconfig import EvaluatorConfig


class EvaluatorConfigManager:
    def __init__(self, config_directory: Union[str, Path]):
        self.config_directory = config_directory

    @property
    def config_directory(self):
        return self._config_directory

    @config_directory.setter
    def config_directory(self, value: Union[str, Path]):
        assert isinstance(value, (str, Path))

        self._config_directory = ensure_path(value, create_dir=True)

    def create_config(
        self,
        name: str,
        description: str,
        author: str,
        filename: Union[str, Path] = None
    ):
        assert isinstance(name, str)
        assert isinstance(description, str)
        assert isinstance(author, str)
        assert (filename is None) or isinstance(filename, (str, Path))

        if not filename:
            # set automatic filename, if not set
            filename = self.config_directory.joinpath(
                f"{name}.yml"
            )

        else:
            # ensure that filename is Path
            filename = ensure_path(filename)

        if filename.exists():
            # file does already exist
            raise FileExistsError(
                f"The config file '{filename}' does already exist!"
            )

        ec = EvaluatorConfig(
            filename=filename,
            name=name,
            description=description,
            author=author
        )
        return ec.save()

    def load_config(self, filename: Union[str, Path]):
        assert isinstance(filename, (str, Path))

        # ensure that filename is Path
        filename = ensure_path(filename)

        return EvaluatorConfig.from_file(filename=filename)
