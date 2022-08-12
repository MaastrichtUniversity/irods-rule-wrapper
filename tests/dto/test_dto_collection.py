import json

from irodsrulewrapper.dto.tape_estimate import TapeEstimate
from irodsrulewrapper.dto.attribute_value import AttributeValue
from irodsrulewrapper.dto.boolean import Boolean
from irodsrulewrapper.dto.collection import Collection
from irodsrulewrapper.dto.collection_details import CollectionDetails
from irodsrulewrapper.dto.collection_sizes import CollectionSizes, CollectionSize
from irodsrulewrapper.dto.collections import Collections
from irodsrulewrapper.dto.external_pid import ExternalPID
from irodsrulewrapper.dto.metadata_pid import MetadataPID


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
    assert collection.num_files == 1253


def test_collections():
    collections = Collections.create_from_rule_result(json.loads(COLLECTIONS_JSON)).collections
    assert collections is not None
    assert collections.__len__() == 2
    assert collections[0].title == "Test Coll 1"
    assert collections[1].title == "Test Coll 2.0"


def test_boolean():
    result = Boolean.create_from_rule_result(BOOLEAN_RESULT)
    assert result.boolean is True


def test_dto_attribute_value():
    ret = AttributeValue.create_from_rule_result(json.loads('{"value": "foobar"}'))
    assert ret.value == "foobar"


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


def test_dto_metadata_pid():
    result = MetadataPID.create_from_rule_result(json.loads(METADATA_PID))
    assert result.collection_pid["handle"] == "21.T12996/P000000014C000000001.1"
    assert result.collection_pid["url"] == "http://mdr.local.dh.unimaas.nl/hdl/P000000014/C000000001.1"

    assert result.instance_pid["handle"] == "21.T12996/P000000014C000000001instance.1"
    assert result.instance_pid["url"] == "http://mdr.local.dh.unimaas.nl/hdl/P000000014/C000000001/instance.1"

    assert result.schema_pid["handle"] == "21.T12996/P000000014C000000001schema.1"
    assert result.schema_pid["url"] == "http://mdr.local.dh.unimaas.nl/hdl/P000000014/C000000001/schema.1"


def test_dto_external_pid():
    pid = ExternalPID.create_from_rule_result(json.loads(EXTERNAL_PID))
    assert pid is not None
    assert pid.pid == "https://doi.org/10.34894/UMF5VF"
    assert pid.repository == "DataverseNL"


def test_dto_tape_estimate():
    estimate = TapeEstimate.create_from_rule_result(json.loads(PROJECT_COLLECTION_TAPE_ESTIMATE))
    assert estimate.above_threshold_bytes_size == 521638758
    assert estimate.above_threshold_number_files == 1
    assert estimate.archivable_bytes_size == 521638758
    assert estimate.archivable_number_files == 1
    assert estimate.status == "online"


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

METADATA_PID = """
{
    "collection": {
        "handle": "21.T12996/P000000014C000000001.1",
        "url": "http://mdr.local.dh.unimaas.nl/hdl/P000000014/C000000001.1"
    },
    "instance": {
        "handle": "21.T12996/P000000014C000000001instance.1",
        "url": "http://mdr.local.dh.unimaas.nl/hdl/P000000014/C000000001/instance.1"
    },
    "schema": {
        "handle": "21.T12996/P000000014C000000001schema.1",
        "url": "http://mdr.local.dh.unimaas.nl/hdl/P000000014/C000000001/schema.1"
    }
}

"""

EXTERNAL_PID = """
{
    "value": "doi:10.34894/UMF5VF",
    "unit": "DataverseNL"
}
"""

PROJECT_COLLECTION_TAPE_ESTIMATE = """
{
    "above_threshold": {
        "bytes_size": 521638758,
        "number_files": 1
    },
    "archivable": {
        "bytes_size": 521638758,
        "number_files": 1
    },
    "status": "online"
}

"""
