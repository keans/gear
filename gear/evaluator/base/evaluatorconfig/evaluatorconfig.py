import datetime
from pathlib import Path
from typing import Union

import yaml

from gear.utils.utils import ensure_path
from gear.evaluator.base.evaluatorconfig.evaluatorconfigvalidator import \
    EvaluatorConfigValidator
from gear.evaluator.base.evaluatorconfig.evaluatorconfigschema import \
    evaluator_config_schema
from gear.evaluator.base.evaluatorexceptions import EvaluatorConfigException


class EvaluatorConfig:
    """
    class to manage evaluator configuration files
    """
    FIELDS = ("name", "description", "author", "filetypes")

    def __init__(
        self,
        filename: str,
        name: str = None,
        description: str = None,
        author: str = None
    ):
        self.filename = filename
        self.name = name
        self.description = description
        self.author = author
        self.filetypes = {}

        # prepare validator
        self.validator = EvaluatorConfigValidator(
            schema=evaluator_config_schema
        )

    @staticmethod
    def from_file(
        filename: Union[str, Path]
    ) -> "EvaluatorConfig":
        """
        load evaluator config from filename

        :param filename: filename
        :type filename: Union[str, Path]
        :return: evaluator config
        :rtype: EvaluatorConfig
        """


        ec = EvaluatorConfig(filename=filename)
        ec.load()

        return ec

    @staticmethod
    def create_file(
        config_directory: Union[str, Path],
        name: str,
        description: str,
        author: str,
    ) -> Path:
        """
        create a new config file

        :param config_directory: directory in which the config should be stored
        :type config_directory: Union[str, Path]
        :param name: name of the configuration (will be name of config file)
        :type name: str
        :param description: description of the configuration
        :type description: str
        :param author: author of the configuration
        :type author: str
        :return: name of the main config file
        :rtype: Path
        """
        assert isinstance(config_directory, (str, Path))
        assert isinstance(name, str)
        assert isinstance(description, str)
        assert isinstance(author, str)

        # ensure directory
        config_directory = ensure_path(config_directory)

        # add config name to directory
        config_directory = config_directory.joinpath(name)
        config_directory.mkdir()

        # prepare configuration filename
        filename = config_directory.joinpath(f"{name}.yml")

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

    @property
    def yaml(self) -> str:
        return yaml.safe_dump(self.dict, sort_keys=False)

    @property
    def dict(self) -> dict:
        """
        returns the dictionary representation of the evaluator config

        :raises EvaluatorConfigException: raised, if evaluator config cannot
                                          be validated
        :return: dictionary of the evaluator config
        :rtype: dict
        """
        d = {
            "name": self.name,
            "description": self.description,
            "author": self.author,
            "creation_date": datetime.datetime.now(),
            "filetypes": self.filetypes,
        }

        if not self.validator.validate(d):
            raise EvaluatorConfigException(
                f"{self.validator.errors}"
            )

        return d

    @property
    def filename(self) -> Path:
        """
        returns the filename

        :return: filename
        :rtype: Path
        """
        return self._filename

    @filename.setter
    def filename(self, value: Union[str, Path]):
        """
        set filename

        :param value: filename
        :type value: Union[str, Path]
        """
        assert isinstance(value, (str, Path))

        self._filename = ensure_path(value)

    def load(self):
        """
        load the evaluator config from file

        :raises EvaluatorConfigException: raised, if validation failed
        """
        # load yaml file
        with self.filename.open("r") as f:
            # load yaml from file
            d = yaml.safe_load(f)

            if not self.validator.validate(d):
                # validation of read file has failed
                raise EvaluatorConfigException(
                    f"{self.validator.errors}"
                )

            # set internal properties
            for field in self.FIELDS:
                setattr(self, field, d[field])

    def save(self) -> Path:
        """
        save evaluator config to filename path

        :return: filena of evaluator config
        :rtype: Path
        """
        with self.filename.open("w") as f:
            yaml.safe_dump(self.dict, f, sort_keys=False)

        return self.filename

    def __repr__(self) -> str:
        """
        returns the string representation of the evaluator config

        :return: string representation of the evaluator config
        :rtype: str
        """
        return (
            f"<EvaluatorConfig(filename='{self.filename}', "
            f"name='{self.name}', "
            f"description='{self.description}', "
            f"author='{self.author}', filetypes={self.filetypes})>"
        )
