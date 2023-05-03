from json import JSONEncoder
from typing import Any

from nested_dict import nested_dict


# nasty json patch to support JSON for custom classes via __json__ method
def wrapped_default(self, obj):
    return getattr(obj.__class__, "__json__", wrapped_default.default)(obj)


# patch default
wrapped_default.default = JSONEncoder().default
JSONEncoder.default = wrapped_default


class FormattedResult:
    """
    class to store a formatted result, i.e., a value and a format
    It can be used as item in the result manager
    """
    def __init__(self, value, fmt=""):
        self.value = value
        self.fmt = fmt

    def __json__(self):
        return {"value": self.value, "fmt": self.fmt}

    def __str__(self):
        return (
            f"<FormattedResult(value={self.value}, fmt='{self.fmt}')"
        )


class ResultManager(nested_dict):
    """
    result manager is a nested dictionary that allows to store
    values easily without the hassle of dealing with the creation
    on sub dictionaries and value types that should be stored
    """
    def __init__(self, level: int):
        nested_dict.__init__(self, level)
        self.level = level

    def _resolve(self, topics: list):
        """
        helper function to go level-wise down in the nested-dict
        until one before final state is reached. This is returned
        and can then be used for further modifications.
        """
        assert len(topics) <= self.level

        d = self
        for k in topics[:-1]:
            d = d[k]

        return d

    def append(self, topics: list, value: Any):
        """
        append a value to the nested dict, identified by its topics

        :param topics: list of topics
        :type topics: list
        :param value: value that should be appended to the list
        :type value: Any
        """
        if not isinstance(self._resolve(topics)[topics[-1]], list):
            # ensure that item is of list type
            self._resolve(topics)[topics[-1]] = list()

        self._resolve(topics)[topics[-1]].append(value)

    def set(self, topics: list, value: Any):
        """
        set a value to the nested dict, identified by its topics

        :param topics: list of topics
        :type topics: list
        :param value: value that should be set
        :type value: Any
        """
        self._resolve(topics)[topics[-1]] = value

    def inc(self, topics: list):
        """
        increase value in the nested dict, identified by its topics

        :param topics: list of topics
        :type topics: list
        """
        if not isinstance(self._resolve(topics)[topics[-1]], int):
            # ensure that item is an integer
            self._resolve(topics)[topics[-1]] = 0

        self._resolve(topics)[topics[-1]] = 1
