"""This module contains the Resource DTO class and its factory constructor."""
from irodsrulewrapper.dto.dto_base_model import DTOBaseModel


class Resource(DTOBaseModel):
    """This class represents an iRODS resource with its minimal attributes."""

    name: str
    comment: str
    available: bool

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "Resource":
        if "available" not in result:
            result["available"] = False
        resource = cls(name=result["name"], comment=result["comment"], available=result["available"])
        return resource
