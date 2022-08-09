import json

from irodsrulewrapper.dto.resource import Resource
from irodsrulewrapper.dto.resources import Resources


def test_dto_resource():
    resource = Resource.create_from_rule_result(json.loads(RESOURCE))
    assert resource is not None
    assert resource.name == "replRescUM01"
    assert resource.comment == "Replicated-resource-for-UM"


def test_dto_resources():
    result = Resources.create_from_rule_result(json.loads(RESOURCES))
    assert result is not None
    assert result.resources.__len__() == 2
    assert result.resources[0].name == "replRescUM01"
    assert result.resources[1].name == "replRescAZM01"


RESOURCE = """
{
    "comment": "Replicated-resource-for-UM",
    "name": "replRescUM01"
}
"""

RESOURCES = """
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
