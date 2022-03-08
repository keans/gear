import re

from cerberus import Validator


class ArgConfigValidator(Validator):
    def _check_with_is_alphanumeric(self, field: str, value: str):
        """
        checks if value is a alphanumeric value or includes one of: _, -, .
        """
        res = re.compile(r"^[A-Za-z0-9._-]+$").match(value)
        if not res:
            self._error(field, f"Invalid alphanumeric string '{value}'!")
