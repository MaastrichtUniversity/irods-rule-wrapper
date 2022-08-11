"""This module contains the AttributeValue DTO class and its factory constructor."""
import json

from irodsrulewrapper.dto.dto_base_model import DTOBaseModel


class AttributeValue(DTOBaseModel):
    """
    This class represents the output value of an AVU query by attribute.

    TO_REFACTOR: AttributeValue & Token are very similar, refactor them as a StringValue DTO (same a Boolean)
    """

    value: str

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "AttributeValue":
        value = cls(value=result["value"])
        return value

    @classmethod
    def create_from_mock_result(cls, mock_json=None) -> "AttributeValue":
        if mock_json is None:
            mock_json = '{"value": "3"}'
        return AttributeValue.create_from_rule_result(json.loads(mock_json))
