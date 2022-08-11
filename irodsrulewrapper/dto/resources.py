"""This module contains the Resources DTO class and its factory constructor."""
from irodsrulewrapper.dto.resource import Resource


class Resources:
    """This class represents a list of iRODS Resource DTOs."""

    def __init__(self, resources: list["Resource"]):
        self.resources: list["Resource"] = resources

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "Resources":
        output = []
        for item in result:
            resource = Resource.create_from_rule_result(item)
            output.append(resource)
        resources = cls(output)
        return resources
