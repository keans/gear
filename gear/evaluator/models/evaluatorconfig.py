import datetime
from pathlib import Path
from typing import Union

import yaml

from gear.utils.utils import ensure_path
from gear.evaluator.cerberusutils.evaluatorconfigvalidator import \
    EvaluatorConfigValidator


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
        self.validator = EvaluatorConfigValidator()

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

    @property
    def dict(self) -> dict:
        d = {
            "name": self.name,
            "description": self.description,
            "author": self.author,
            "creation_date": datetime.datetime.now(),
            "filetypes": {},
        }

        if not self.validator.validate(d):
            raise Exception(
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
        # load yaml file
        with self.filename.open("r") as f:
            d = yaml.safe_load(f)
            if not self.validator.validate(d):
                raise Exception(
                    f"{self.validator.errors}"
                )

            # set internal properties
            for field in self.FIELDS:
                setattr(self, field, d[field])

    def save(self) -> Path:
        with self.filename.open("w") as f:
            yaml.safe_dump(self.dict, f, sort_keys=False)

        return self.filename

    def __repr__(self) -> str:
        return (
            f"<EvaluatorConfig(filename='{self.filename}', "
            f"name='{self.name}', "
            f"description='{self.description}', "
            f"author='{self.author}', filetypes={self.filetypes})>"
        )

