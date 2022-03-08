from typing import Any

from gear.base.argconfig.argconfigvalidator import ArgConfigValidator


class ArgConfigException(Exception):
    """
    argument configuration exception
    """


class ArgConfig:
    def __init__(
        self,
        argconfig_schema: dict,
        d: dict
    ):
        self.validator = ArgConfigValidator(argconfig_schema)
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
        assert (value is None) or isinstance(value, dict)

        if value is None:
            # value set to None
            self._dict = None

        else:
            # dict provided then validate it
            self._dict = value
            if not self.validator.validate(self._dict):
                # invalid configuration arguments
                raise ArgConfigException(self.validator.errors)

    def __repr__(self) -> str:
        return (
            f"<ArgConfig(dict={self.dict})>"
        )
