import json

from irodsrulewrapper.dto.boolean import Boolean
from irodsrulewrapper.dto.collection import Collection
from irodsrulewrapper.dto.collection_details import CollectionDetails
from irodsrulewrapper.dto.collection_sizes import CollectionSizes, CollectionSize
from irodsrulewrapper.dto.collections import Collections


# AttributeValue
# TapeEstimate
# CollectionDetails
def test_collection_details():
    collection = CollectionDetails.create_from_rule_result(json.loads(COLLECTION_DETAILS))
    assert collection is not None
    assert collection.title == "Dataset Title1"
    assert collection.pid == "21.T12996/P000000014C000000001"
    assert collection.creator == "jonathan.melius@maastrichtuniversity.nl"
    assert collection.size == 554400
    assert collection.num_files == "4"


def test_collection():
    collection = Collection.create_from_rule_result(json.loads(COLLECTION_JSON))
    assert collection is not None
    assert collection.title == "Test Coll 1"
    assert collection.pid == "21.T12996/P000000010C000000001"
    assert collection.creator == "jonathan.melius@maastrichtuniversity.nl"
    assert collection.size == 2793.9677238464355
    assert collection.num_files == "1253"


def test_collections():
    collections = Collections.create_from_rule_result(json.loads(COLLECTIONS_JSON)).collections
    assert collections is not None
    assert collections.__len__() == 2
    assert collections[0].title == "Test Coll 1"
    assert collections[1].title == "Test Coll 2.0"


def test_boolean():
    result = Boolean.create_from_rule_result(BOOLEAN_RESULT)
    assert result.boolean is True


def test_dto_collection_size():
    result = CollectionSize.create_from_rule_result(json.loads(COLLECTION_SIZE_PER_RESOURCE))
    assert result.relative_size == 72.9
    assert result.resource == "replRescUM01"
    assert result.size == 270572544


def test_dto_collections_sizes():
    result = CollectionSizes.create_from_rule_result(json.loads(COLLECTIONS_SIZE_PER_RESOURCE))
    assert len(result.collection_sizes["C000000001"]) == 2
    assert len(result.collection_sizes) == 3

    assert result.collection_sizes["C000000001"][1].relative_size == 27.1
    assert result.collection_sizes["C000000001"][1].resource == "arcRescSURF01"
    assert result.collection_sizes["C000000001"][1].size == 100719825

    assert result.collection_sizes["C000000002"][0].relative_size == 100.0
    assert result.collection_sizes["C000000002"][0].resource == "replRescUM01"
    assert result.collection_sizes["C000000002"][0].size == 371251334

    assert result.collection_sizes["C000000003"][0].relative_size == 100.0
    assert result.collection_sizes["C000000003"][0].resource == "replRescUM01"
    assert result.collection_sizes["C000000003"][0].size == 3734


COLLECTION_SIZE_PER_RESOURCE = """
{     
    "relativeSize": 72.9,
    "resourceId": "10160",
    "resourceName": "replRescUM01",
    "size": "270572544"
}
"""

COLLECTIONS_SIZE_PER_RESOURCE = """
{
    "C000000001": [
        {
            "relativeSize": 72.9,
            "resourceId": "10160",
            "resourceName": "replRescUM01",
            "size": "270572544"
        },
        {
            "relativeSize": 27.1,
            "resourceId": "10017",
            "resourceName": "arcRescSURF01",
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

BOOLEAN_RESULT = True

COLLECTION_JSON = """
{
    "PID": "21.T12996/P000000010C000000001",
    "creator": "jonathan.melius@maastrichtuniversity.nl",
    "id": "C000000001",
    "numFiles": "1253",
    "numUserFiles": 1251,
    "size": 2793.9677238464355,
    "title": "Test Coll 1"
}
"""

COLLECTIONS_JSON = """
[
    {
        "PID": "21.T12996/P000000010C000000001",
        "creator": "jonathan.melius@maastrichtuniversity.nl",
        "id": "C000000001",
        "numFiles": "1253",
        "numUserFiles": 1251,
        "size": 2793.9677238464355,
        "title": "Test Coll 1"
    },
    {
        "PID": "21.T12996/P000000010C000000002",
        "creator": "jonathan.melius@maastrichtuniversity.nl",
        "id": "C000000002",
        "numFiles": "42",
        "numUserFiles": 40,
        "size": 0.0,
        "title": "Test Coll 2.0"
    }
]
"""

COLLECTION_DETAILS = """
{
    "PID": "21.T12996/P000000014C000000001",
    "byteSize": 554400,
    "collection": "C000000001",
    "contributors": {
        "groupObjects": [
            {
                "description": "It's DataHub! The place to store your data.",
                "displayName": "DataHub",
                "groupId": "10122",
                "groupName": "datahub"
            }
        ],
        "groups": [
            "datahub"
        ],
        "userObjects": [
            {
                "displayName": "service-pid",
                "userId": "10107",
                "userName": "service-pid"
            }
        ],
        "users": [
            "service-pid"
        ]
    },
    "creator": "jonathan.melius@maastrichtuniversity.nl",
    "enableArchive": "true",
    "enableOpenAccessExport": "true",
    "enableUnarchive": "true",
    "exporterState": "no-state-set",
    "externals": "no-externalPID-set",
    "managers": {
        "groupObjects": [],
        "groups": [],
        "userObjects": [
            {
                "displayName": "Pascal Suppers",
                "userId": "10058",
                "userName": "psuppers"
            },
            {
                "displayName": "Olav Palmen",
                "userId": "10083",
                "userName": "opalmen"
            }
        ],
        "users": [
            "psuppers",
            "opalmen"
        ]
    },
    "numFiles": "4",
    "project": "P000000014",
    "title": "Dataset Title1",
    "viewers": {
        "groupObjects": [],
        "groups": [],
        "userObjects": [
            {
                "displayName": "service-disqover",
                "userId": "10110",
                "userName": "service-disqover"
            }
        ],
        "users": [
            "service-disqover"
        ]
    }
}
"""
