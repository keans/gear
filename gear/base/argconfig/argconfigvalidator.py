import re

from cerberus import Validator


class ArgConfigValidator(Validator):
    """
    validator of the argument configuration
    """
    def _check_with_is_alphanumeric(self, field: str, value: str):
        """
        checks if value is a alphanumeric value or includes one of: _, -, .

        :param field: field
        :type field: str
        :param value: value
        :type value: str
        """
        res = re.compile(r"^[A-Za-z0-9._-]+$").match(value)
        if not res:
            # invalid value
            self._error(field, f"Invalid alphanumeric string '{value}'!")
