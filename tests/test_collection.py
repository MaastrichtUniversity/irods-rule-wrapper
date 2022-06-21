import pytest

from irodsrulewrapper.dto.boolean import Boolean
from irodsrulewrapper.dto.collection import Collection
from irodsrulewrapper.dto.collections import Collections
from irodsrulewrapper.rule import RuleManager, RuleJSONManager
from irodsrulewrapper.utils import publish_message
import json
from irods.exception import CAT_NO_ACCESS_PERMISSION


@pytest.mark.skip(reason="needs local setup first.")
def test_publish_message():
    message = {
        "project": "P000000015",
        "collection": "C000000002",
        "repository": "Dataverse",
        "dataverse_alias": "DataHub",
        "restrict": False,
        "restrict_list": "P000000015/C000000002/specialchars_~!@#$%^&()-+=[]{};',.txt,\tP000000015/C000000002/test.log",
        "data_export": False,
        "delete": False,
        "depositor": "jonathan.melius@maastrichtuniversity.nl",
    }
    json_message = json.dumps(message)
    publish_message("datahub.events_tx", "projectCollection.exporter.requested", json_message)
    assert True is True


@pytest.mark.skip(reason="needs local setup first.")
def test_export_project_collection_by_step():
    project = "P000000015"
    collection = "C000000002"
    repository = "Dataverse"

    RuleManager(admin_mode=True).prepare_export(project, collection, repository)

    message = {
        "project": project,
        "collection": collection,
        "repository": repository,
        "dataverse_alias": "DataHub",
        "restrict": False,
        "restrict_list": "P000000015/C000000002/specialchars_~!@#$%^&()-+=[]{};\"',.txt,\tP000000015/C000000002/test.log",
        "data_export": False,
        "delete": False,
        "depositor": "jonathan.melius@maastrichtuniversity.nl",
    }
    json_message = json.dumps(message)
    publish_message("datahub.events_tx", "projectCollection.exporter.requested", json_message)
    assert True is True


@pytest.mark.skip(reason="needs local setup first.")
def test_rule_export_project_collection():
    project = "P000000015"
    collection = "C000000002"
    repository = "Dataverse"
    message = {
        "project": project,
        "collection": collection,
        "repository": repository,
        "dataverse_alias": "DataHub",
        "restrict": False,
        "restrict_list": "P000000015/C000000002/specialchars_~!@#$%^&()-+=[]{};\"',.txt,\tP000000015/C000000002/test.log",
        "data_export": False,
        "delete": False,
        "depositor": "jonathan.melius@maastrichtuniversity.nl",
    }
    RuleManager(admin_mode=True).export_project_collection(project, collection, repository, message)

    assert True is True


def test_rule_get_collection_avu():
    avu = RuleManager(admin_mode=True).get_collection_attribute_value("/nlmumc/projects/P000000010/C000000001", "title")
    assert avu is not None


def test_get_project_collection_tape_estimate():
    collection = RuleManager(admin_mode=True).get_project_collection_tape_estimate("P000000010", "C000000001")
    assert collection is not None


def test_rule_get_collection_tree():
    collection = RuleJSONManager(admin_mode=True).get_collection_tree("P000000010/C000000001")
    assert collection is not None


def test_rule_get_project_collection_details():
    collection = RuleManager(admin_mode=True).get_project_collection_details("P000000011", "C000000001", "false")
    assert collection is not None
    assert collection.id == "C000000001"
    assert collection.creator == "irods_bootstrap@docker.dev"
    assert collection.title == "(HVC) Placeholder collection"
    assert collection.enable_archive is False
    assert collection.enable_open_access_export is False


def test_rule_get_collections():
    result = RuleManager(admin_mode=True).get_collections("/nlmumc/projects/P000000011")
    collections = result.collections
    assert collections is not None
    assert collections[0].creator == "irods_bootstrap@docker.dev"


@pytest.mark.skip(reason="needs local setup first.")
def test_rule_get_collections_var_config():
    config = dict()
    config["IRODS_HOST"] = "0.0.0.0"
    config["IRODS_USER"] = "rods"
    config["IRODS_PASS"] = "irods"
    result = RuleManager(config=config).get_collections("/nlmumc/projects/P000000011")
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


def test_boolean():
    result = Boolean.create_from_rule_result(BOOLEAN_RESULT)
    assert result.boolean is True


BOOLEAN_RESULT = True

COLLECTION_JSON = """
{
    "PID": "21.T12996/P000000010C000000001",
    "creator": "jonathan.melius@maastrichtuniversity.nl",
    "id": "C000000001",
    "numFiles": "1253",
    "numUserFiles": "1249",
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
        "numUserFiles": "1249",
        "size": 2793.9677238464355,
        "title": "Test Coll 1"
    },
    {
        "PID": "21.T12996/P000000010C000000002",
        "creator": "jonathan.melius@maastrichtuniversity.nl",
        "id": "C000000002",
        "numFiles": "42",
        "numUserFiles": "38",
        "size": 0.0,
        "title": "Test Coll 2.0"
    }
]
"""


@pytest.mark.skip()
def test_rule_export():
    result = False
    try:
        # RuleManager(admin_mode=True).export_project_collection("P000000016", "C000000001", "DataverseNL", {})
        RuleManager("mcoonen").export_project_collection("P000000016", "C000000001", "DataverseNL", {})
    except CAT_NO_ACCESS_PERMISSION:
        result = True

    assert result is True


@pytest.mark.skip()
def test_rule_archive():
    result = False
    try:
        # RuleManager("service-surfarchive").archive_project_collection("/nlmumc/projects/P000000016/C000000001")
        RuleManager("jmelius").archive_project_collection("/nlmumc/projects/P000000015/C000000001")
    except CAT_NO_ACCESS_PERMISSION:
        result = True

    assert result is True
