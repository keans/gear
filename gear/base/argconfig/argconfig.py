from typing import Any, Union

from luigi.freezing import FrozenOrderedDict

from gear.base.argconfig.argconfigvalidator import ArgConfigValidator
from gear.base.exceptions import ArgConfigException


class ArgConfig:
    """
    argument configuration for plugins
    """
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

    def contains(self, key: str) -> bool:
        """
        returns True, if configuration conatins given key

        :param key: key to be queried
        :type key: str
        :return: True, if key is in configuration
        :rtype: bool
        """
        return (key in self.dict)

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
        """
        return the string representation of the argument configuration

        :return: string representation of the argument configuration
        :rtype: str
        """
        return (
            f"<ArgConfig(dict={self.dict})>"
        )
