"""This module contains the Boolean DTO class and its factory constructor."""


class Boolean:
    """This class represents a boolean rule output."""

    def __init__(self, boolean: bool):
        self.boolean: bool = boolean

    @classmethod
    def create_from_rule_result(cls, result: bool) -> "Boolean":
        boolean = cls(result)
        return boolean
