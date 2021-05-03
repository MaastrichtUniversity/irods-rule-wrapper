from irodsrulewrapper.dto.collection import Collection
from irodsrulewrapper.dto.collections import Collections
from irodsrulewrapper.rule import RuleManager
import json


def test_rule_get_collection_avu():
    avu = RuleManager().get_collection_attribute_value("/nlmumc/projects/P000000010/C000000001", "title")
    assert avu is not None


def test_get_project_collection_tape_estimate():
    collection = RuleManager().get_project_collection_tape_estimate("P000000010", "C000000001")
    assert collection is not None


def test_rule_get_collection_tree():
    collection = RuleManager().get_collection_tree("P000000010/C000000001", "P000000010/C000000001")
    assert collection is not None


def test_rule_get_project_collection_details():
    collection = RuleManager().get_project_collection_details("P000000011", "C000000001", "false")
    assert collection is not None
    assert collection.id == "C000000001"
    assert collection.creator == "irods_bootstrap@docker.dev"
    assert collection.title == "(HVC) Placeholder collection"
    assert collection.enable_archive is False
    assert collection.enable_open_access_export is False


def test_rule_get_collections():
    result = RuleManager().get_collections("/nlmumc/projects/P000000011")
    collections = result.collections
    assert collections is not None
    assert collections[0].creator == "irods_bootstrap@docker.dev"


def test_collection():
    collection = Collection.create_from_rule_result(json.loads(COLLECTION_JSON))
    assert collection is not None
    assert collection.title == "Test Coll 1"
    assert collection.pid == "21.T12996/P000000010C000000001"
    assert collection.creator == "jonathan.melius@maastrichtuniversity.nl"
    assert collection.size == 2793.9677238464355
    assert collection.num_files == "1253"


def test_collections():
    result = Collections.create_from_rule_result(json.loads(COLLECTIONS_JSON))
    collections = result.collections
    assert collections is not None
    assert collections.__len__() == 2
    assert collections[0].title == "Test Coll 1"
    assert collections[1].title == "Test Coll 2.0"


COLLECTION_JSON = '''
{
    "PID": "21.T12996/P000000010C000000001",
    "creator": "jonathan.melius@maastrichtuniversity.nl",
    "id": "C000000001",
    "numFiles": "1253",
    "size": 2793.9677238464355,
    "title": "Test Coll 1"
}
'''

COLLECTIONS_JSON = '''
[
    {
        "PID": "21.T12996/P000000010C000000001",
        "creator": "jonathan.melius@maastrichtuniversity.nl",
        "id": "C000000001",
        "numFiles": "1253",
        "size": 2793.9677238464355,
        "title": "Test Coll 1"
    },
    {
        "PID": "21.T12996/P000000010C000000002",
        "creator": "jonathan.melius@maastrichtuniversity.nl",
        "id": "C000000002",
        "numFiles": "42",
        "size": 0.0,
        "title": "Test Coll 2.0"
    }
]
'''

