import re

from cerberus import Validator

from gear.evaluator.cerberusutils.evaluatorconfigschema import \
    evaluator_config_schema


class EvaluatorConfigValidator(Validator):
    def __init__(self, *args, **kwargs):
        Validator.__init__(
            self, evaluator_config_schema, *args, **kwargs
        )

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
        res = re.compile(r'^(?:"?([^"]*)"?\s)?(?:<?(.+@[^>]+)>?)$').match(value)
        if not res:
            self._error(field, f"Invalid author '{value}'!")
