import re

from cerberus import Validator


class EvaluatorConfigValidator(Validator):
    def _check_with_is_alphanumeric(self, field: str, value: str):
        """
        checks if value is a alphanumeric value or includes one of: _, -, .
        """
        res = re.compile(r"^[A-Za-z0-9._-]+$").match(value)
        if not res:
            self._error(field, f"Invalid alphanumeric string '{value}'!")

    def _check_with_is_author(self, field: str, value: str):
        """
        checks if value is a author value of the format
        Firstname Lastname <email@example.com>
        """
        res = re.compile(
            r'^(?:"?([^"]*)"?\s)?(?:<?(.+@[^>]+)>?)$'
        ).match(value)
        if not res:
            self._error(field, f"Invalid author '{value}'!")
