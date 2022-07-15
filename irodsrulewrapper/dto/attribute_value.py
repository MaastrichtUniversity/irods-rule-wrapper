"""
This module contains the AttributeValue DTO class and its factory constructor
"""


class AttributeValue:
    """
    This class represents the output value of an AVU query by attribute.

    TO_REFACTOR: AttributeValue & Token are very similar, refactor them as a StringValue DTO (same a Boolean)
    """

    def __init__(self, value: str):
        self.value: str = value

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "AttributeValue":
        value = cls(result["value"])
        return value
