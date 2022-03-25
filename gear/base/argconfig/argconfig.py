from typing import Any, Union

from luigi.freezing import FrozenOrderedDict

from gear.base.argconfig.argconfigvalidator import ArgConfigValidator


class ArgConfigException(Exception):
    """
    argument configuration exception
    """


class ArgConfig:
    def __init__(
        self,
        schema: dict,
        d: Union[dict, FrozenOrderedDict] = {}
    ):
        self.validator = ArgConfigValidator(schema)
        self.dict = d

    def __getitem__(self, key: str) -> Any:
        """
        get item

        :param key: key
        :type key: Any
        :return: name of the key
        :rtype: str
        """
        return self.dict.get(key, None)

    @property
    def dict(self) -> dict:
        """
        returns the dict

        :return: dict
        :rtype: dict
        """
        return self._dict

    @dict.setter
    def dict(self, value: dict):
        """
        set dict

        :param value: dict
        :type value: dict
        """
        assert isinstance(value, (dict, FrozenOrderedDict))

        self._dict = value
        if (value != {}) and not self.validator.validate(self._dict):
            # non-empty dict provided and invalid configuration arguments
            raise ArgConfigException(self.validator.errors)

    def __repr__(self) -> str:
        return (
            f"<ArgConfig(dict={self.dict})>"
        )
