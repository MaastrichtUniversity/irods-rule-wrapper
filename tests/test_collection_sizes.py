from irodsrulewrapper.dto.collection_sizes import CollectionSizes
from irodsrulewrapper.rule import RuleManager

import json


def test_rule_get_collection_size_per_resource():
    result = RuleManager("rodsadmin").get_collection_size_per_resource("P000000017")
    assert result is not None


def test_dto_collection_sizes():
    result = CollectionSizes.create_from_rule_result(json.loads(COLLECTION_SIZE_PER_RESOURCE))
    assert result is not None
    assert len(result.collection_sizes["C000000001"]) == 2
    assert len(result.collection_sizes) == 3
    assert result.collection_sizes["C000000001"][0].relative_size is not None
    assert result.collection_sizes["C000000001"][0].resource is not None
    assert result.collection_sizes["C000000001"][0].size is not None


COLLECTION_SIZE_PER_RESOURCE = """
{
    "C000000001": [
        {
            "relativeSize": 72.9,
            "resourceId": "10017",
            "resourceName": "arcRescSURF01",
            "size": "270572544"
        },
        {
            "relativeSize": 27.1,
            "resourceId": "10160",
            "resourceName": "replRescUM01",
            "size": "100719825"
        }
    ],
    "C000000002": [
        {
            "relativeSize": 100.0,
            "resourceId": "10160",
            "resourceName": "replRescUM01",
            "size": "371251334"
        }
    ],
    "C000000003": [
        {
            "relativeSize": 100.0,
            "resourceId": "10160",
            "resourceName": "replRescUM01",
            "size": "3734"
        }
    ]
}
"""
