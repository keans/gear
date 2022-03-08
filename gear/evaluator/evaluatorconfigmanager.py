from typing import Union
from pathlib import Path

from gear.utils.utils import ensure_path
from gear.evaluator.base.evaluatorconfig.evaluatorconfig import \
    EvaluatorConfig


class EvaluatorConfigManager:
    """
    evaluator config manager
    """
    def __init__(
        self,
        config_directory: Union[str, Path]
    ):
        self.config_directory = config_directory

    @property
    def configurations(self) -> list:
        """
        returns a list of all existing configurations in
        the configuration directory

        :return: list of configurations
        :rtype: list
        """
        return self.config_directory.glob("*.yml")

    @property
    def config_directory(self) -> Path:
        """
        returns configuration directory

        :return: configuration directory
        :rtype: Path
        """
        return self._config_directory

    @config_directory.setter
    def config_directory(self, value: Union[str, Path]):
        """
        set configuration directory

        :param value: directory
        :type value: Union[str, Path]
        """
        assert isinstance(value, (str, Path))

        self._config_directory = ensure_path(value, create_dir=True)

    def create_config(
        self,
        name: str,
        description: str,
        author: str,
        filename: Union[str, Path] = None
    ) -> Path:
        """
        create a new configuration

        :param name: name of the configuration
        :type name: str
        :param description: description of the configuration
        :type description: str
        :param author: author of the configuration
        :type author: str
        :param filename: filename of the configuration, defaults to None
        :type filename: Union[str, Path], optional
        :raises FileExistsError: raised, if file does not exist
        :return: path of the created configuration file
        :rtype: Path
        """
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

        # prepare new config file
        ec = EvaluatorConfig(
            filename=filename,
            name=name,
            description=description,
            author=author
        )
        return ec.save()

    def load_config(
        self,
        filename: Union[str, Path]
    ) -> EvaluatorConfig:
        """
        load configuration from given file

        :param filename: configuration filename
        :type filename: Union[str, Path]
        :return: loaded configuration
        :rtype: EvaluatorConfig
        """
        assert isinstance(filename, (str, Path))

        # ensure that filename is Path
        filename = ensure_path(filename)

        return EvaluatorConfig.from_file(filename=filename)
