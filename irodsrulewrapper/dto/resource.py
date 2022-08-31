"""This module contains the Resource DTO class and its factory constructor."""


class Resource:
    """This class represents an iRODS resource with its minimal attributes."""

    def __init__(self, name: str, comment: str, available: bool):
        self.name: str = name
        self.comment: str = comment
        self.available: bool = available

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "Resource":
        if "available" not in result:
            result["available"] = False
        resource = cls(result["name"], result["comment"], result["available"])
        return resource
