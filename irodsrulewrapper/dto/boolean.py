"""This module contains the Boolean DTO class and its factory constructor."""
import json


class Boolean:
    """This class represents a boolean rule output."""

    def __init__(self, boolean: bool):
        self.boolean: bool = boolean

    @classmethod
    def create_from_rule_result(cls, result: bool) -> "Boolean":
        boolean = cls(result)
        return boolean

    @classmethod
    def create_from_mock_result(cls, mock_json=None) -> "Boolean":
        if mock_json is None:
            mock_json = True
        return Boolean.create_from_rule_result(mock_json)
