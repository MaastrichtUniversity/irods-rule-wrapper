"""This module contains the Resources DTO class and its factory constructor."""
import json

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

    @classmethod
    def create_from_mock_result(cls, mock_json=None) -> "Resources":
        if mock_json is None:
            mock_json = cls.MOCK_JSON
        return cls.create_from_rule_result(json.loads(mock_json))

    MOCK_JSON = """
    [
        {
            "comment": "Replicated-resource-for-UM",
            "name": "replRescUM01"
        },
        {
            "comment": "Replicated-resource-for-AZM",
            "name": "replRescAZM01"
        }
    ]
    """
