"""This module contains the IntegerValue DTO class and its factory constructor."""
from irodsrulewrapper.dto.dto_base_model import DTOBaseModel


class IntegerValue(DTOBaseModel):
    """IntegerValue"""

    result: int

    @classmethod
    def create_from_rule_result(cls, result: int) -> "IntegerValue":
        user = cls(result=result)
        return user
