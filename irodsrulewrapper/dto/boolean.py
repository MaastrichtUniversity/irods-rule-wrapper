"""This module contains the Boolean DTO class and its factory constructor."""
from irodsrulewrapper.dto.dto_base_model import DTOBaseModel


class Boolean(DTOBaseModel):
    """This class represents a boolean rule output."""

    boolean: bool

    @classmethod
    def create_from_rule_result(cls, result: bool) -> "Boolean":
        boolean = cls(boolean=result)
        return boolean

    @classmethod
    def create_from_mock_result(cls, mock_json=None) -> "Boolean":
        if mock_json is None:
            mock_json = True
        return Boolean.create_from_rule_result(mock_json)
