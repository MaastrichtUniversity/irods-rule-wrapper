import json

from irodsrulewrapper.dto.active_proces import ActiveProcess
from irodsrulewrapper.dto.active_processes import ActiveProcesses
from irodsrulewrapper.dto.data_stewards import DataStewards, DataSteward
from irodsrulewrapper.dto.user_extended import UserExtended
from irodsrulewrapper.dto.user_or_group import UserOrGroup
from irodsrulewrapper.dto.users import Users, User


def test_dto_user():
    user = User.create_from_rule_result(json.loads(PROJECT_USER))
    assert user is not None
    assert user.user_name == "jmelius"
    assert user.user_id == "10068"
    assert user.display_name == "Jonathan Melius"


def test_dto_users():
    result = Users.create_from_mock_result()
    assert result is not None
    assert result.users.__len__() == 19
    assert result.users[0].user_name == "jmelius"
    assert result.users[6].user_name == "auser"


def test_dto_user_extended():
    result = UserExtended.create_from_mock_result()
    assert result is not None
    assert result.display_name == "Olav Palmen"
    assert result.username == "opalmen"


PROJECT_USER = """
{
    "displayName": "Jonathan Melius",
    "userId": "10068",
    "userName": "jmelius"
}
"""


def test_dto_data_steward():
    user = DataSteward.create_from_rule_result(json.loads(DATA_STEWARD))
    assert user is not None
    assert user.user_name == "opalmen"
    assert user.user_id == "10098"
    assert user.display_name == "Olav Palmen"


def test_dto_data_stewards():
    result = DataStewards.create_from_rule_result(json.loads(DATA_STEWARDS))
    assert result is not None
    assert result.data_stewards.__len__() == 3
    assert result.data_stewards[0].user_name == "opalmen"
    assert result.data_stewards[1].user_name == "pvanschay2"


def test_dto_user_or_group():
    user = UserOrGroup.create_from_rule_result(json.loads(USER)).result
    assert user is not None
    assert user["userName"] == "jmelius"
    assert user["userId"] == "10045"
    assert user["account_type"] == "rodsuser"

    group = UserOrGroup.create_from_rule_result(json.loads(GROUP)).result
    assert group is not None
    assert group["groupName"] == "datahub"
    assert group["groupId"] == "10129"
    assert group["account_type"] == "rodsgroup"


def test_dto_active_process():
    active_process = ActiveProcess.create_from_rule_result(json.loads(ACTIVE_PROCESS))
    assert active_process.collection_id == "C000000001"
    assert active_process.project_id == "P000000001"
    assert active_process.project_title == "(UM) Test project #01"
    assert active_process.collection_title == "Title"


def test_dto_active_processes():
    active_processes = ActiveProcesses.create_from_rule_result(json.loads(ACTIVE_PROCESSES))
    assert active_processes.in_progress[0].process_type == "drop_zone"

    assert active_processes.in_progress[1].collection_id == "C000000001"
    assert active_processes.in_progress[1].project_id == "P000000009"
    assert active_processes.in_progress[1].project_title == "(S3-GL) Test project #02"
    assert active_processes.in_progress[1].collection_title == "Dataset1"
    assert active_processes.in_progress[1].process_type == "archive"

    assert active_processes.in_progress[2].process_type == "export"
    assert active_processes.in_progress[3].process_type == "unarchive"

    assert active_processes.open[0].creator == "test_manager"
    assert active_processes.open[0].project == "P000000014"
    assert active_processes.open[0].project_title == "PROJECTNAME"
    assert active_processes.open[0].state == "open"

    assert active_processes.error[0].destination == "C000000001"
    assert active_processes.error[0].project == "P000000014"
    assert active_processes.error[0].project_title == "PROJECTNAME"
    assert active_processes.error[0].state == "error-post-ingestion"

    assert active_processes.completed[0].destination == "C000000001"
    assert active_processes.completed[0].project == "P000000014"
    assert active_processes.completed[0].project_title == "PROJECTNAME"
    assert active_processes.completed[0].state == "ingested"
    assert active_processes.completed[0].percentage_ingested == 100


USER = """
{
    "account_type": "rodsuser",
    "displayName": "Jonathan M\u00e9lius",
    "userId": "10045",
    "userName": "jmelius"
}

"""

GROUP = """
{
    "account_type": "rodsgroup",
    "description": "It's DataHub! The place to store your data.",
    "displayName": "DataHub",
    "groupId": "10129",
    "groupName": "datahub"
}
"""

DATA_STEWARD = """
{
    "displayName": "Olav Palmen",
    "userId": "10098",
    "userName": "opalmen"
}
"""

DATA_STEWARDS = """
[
    {
        "displayName": "Olav Palmen",
        "userId": "10098",
        "userName": "opalmen"
    },
    {
        "displayName": "Paul van Schayck",
        "userId": "10028",
        "userName": "pvanschay2"
    },
    {
        "displayName": "Jonathan Melius",
        "userId": "10068",
        "userName": "jmelius"
    }
]
"""

ACTIVE_PROCESS = """
{
    "collection_id": "C000000001",
    "collection_title": "Title",
    "process_id": "11310",
    "process_type": "archive",
    "project_id": "P000000001",
    "project_title": "(UM) Test project #01",
    "repository": "SURFSara Tape",
    "state": "archive-in-progress 1/1"
}
"""

ACTIVE_PROCESSES = """
{
    "completed": [
        {
            "creator": "test_manager",
            "date": "01676630173",
            "destination": "C000000001",
            "enableDropzoneSharing": "true",
            "percentage_ingested": 100,
            "process_type": "drop_zone",
            "project": "P000000014",
            "projectTitle": "PROJECTNAME",
            "sharedWithMe": "true",
            "state": "ingested",
            "title": "collection_title",
            "token": "strange-tarantula",
            "totalSize": "262347618",
            "type": "direct",
            "validateMsg": "N/A",
            "validateState": "N/A"
        }
    ],
    "error": [
        {
            "creator": "jmelius",
            "date": "01676631376",
            "destination": "C000000001",
            "enableDropzoneSharing": "true",
            "percentage_ingested": 100.0,
            "process_type": "drop_zone",
            "project": "P000000014",
            "projectTitle": "PROJECTNAME",
            "sharedWithMe": "false",
            "state": "error-post-ingestion",
            "title": "collection_title",
            "token": "ashamed-oyster",
            "totalSize": "203618",
            "type": "direct",
            "validateMsg": "N/A",
            "validateState": "N/A"
        },
        {
            "creator": "jmelius",
            "date": "01676626131",
            "destination": "C000000001",
            "enableDropzoneSharing": "true",
            "percentage_ingested": 0,
            "process_type": "drop_zone",
            "project": "P000000002",
            "projectTitle": "(UM) Test project #02",
            "sharedWithMe": "false",
            "state": "error-post-ingestion",
            "title": "Dataset",
            "token": "yucky-elk",
            "totalSize": "0",
            "type": "mounted",
            "validateMsg": "N/A",
            "validateState": "N/A"
        }
    ],
    "in_progress": [
        {
            "creator": "foobar",
            "date": "01676631887",
            "destination": "C000000001",
            "enableDropzoneSharing": "",
            "percentage_ingested": 0,
            "process_type": "drop_zone",
            "project": "P000000015",
            "projectTitle": "",
            "sharedWithMe": "true",
            "state": "validating",
            "title": "collection_title",
            "token": "magnificent-salamander",
            "totalSize": "203618",
            "type": "direct",
            "validateMsg": "N/A",
            "validateState": "N/A"
        },
        {
            "collection_id": "C000000001",
            "collection_title": "Dataset1",
            "process_id": "11308",
            "process_type": "archive",
            "project_id": "P000000009",
            "project_title": "(S3-GL) Test project #02",
            "repository": "SURFSara Tape",
            "state": "complete1"
        },
        {
            "collection_id": "C000000001",
            "collection_title": "Dataset1",
            "process_id": "11307",
            "process_type": "export",
            "project_id": "P000000009",
            "project_title": "(S3-GL) Test project #02",
            "repository": "dataverse",
            "state": "in-queue1"
        },
        {
            "collection_id": "C000000001",
            "collection_title": "Dataset1",
            "process_id": "11309",
            "process_type": "unarchive",
            "project_id": "P000000009",
            "project_title": "(S3-GL) Test project #02",
            "repository": "SURFSara Tape",
            "state": "hola"
        },
        {
            "collection_id": "C000000002",
            "collection_title": "Test1",
            "process_id": "11318",
            "process_type": "unarchive",
            "project_id": "P000000009",
            "project_title": "(S3-GL) Test project #02",
            "repository": "SURFSara Tape",
            "state": "in-queue1"
        }
    ],
    "open": [
        {
            "creator": "test_manager",
            "date": "01676629090",
            "destination": "C000000001",
            "enableDropzoneSharing": "true",
            "percentage_ingested": 0.0,
            "process_type": "drop_zone",
            "project": "P000000014",
            "projectTitle": "PROJECTNAME",
            "sharedWithMe": "true",
            "state": "open",
            "title": "collection_title",
            "token": "talented-fish",
            "totalSize": "262347618",
            "type": "direct",
            "validateMsg": "N/A",
            "validateState": "N/A"
        }
    ]
}
"""
