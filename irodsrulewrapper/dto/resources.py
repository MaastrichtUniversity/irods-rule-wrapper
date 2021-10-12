from .resource import Resource
from typing import List, Dict


class Resources:
    def __init__(self, resources: List["Resource"]):
        self.resources: List["Resource"] = resources

    @classmethod
    def create_from_rule_result(cls, result: Dict) -> "Resources":
        output = []
        for item in result:
            resource = Resource.create_from_rule_result(item)
            output.append(resource)
        resources = cls(output)
        return resources
