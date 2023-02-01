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
    assert result.users.__len__() == 20
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
    assert active_process.collection == "C000000001"
    assert active_process.project == "P000000001"
    assert active_process.project_title == "(UM) Test project #01"
    assert active_process.title == "Title"
def test_dto_active_processes():
    active_processes = ActiveProcesses.create_from_rule_result(json.loads(ACTIVE_PROCESSES))
    assert active_processes.archives[0].collection == "C000000001"
    assert active_processes.archives[0].project == "P000000001"
    assert active_processes.archives[0].project_title == "(UM) Test project #01"
    assert active_processes.archives[0].title == "Title"

    assert active_processes.drop_zones[0].creator == "jmelius"
    assert active_processes.drop_zones[0].project == "P000000001"
    assert active_processes.drop_zones[0].project_title == "(UM) Test project #01"
    assert active_processes.drop_zones[0].state == "open"

    assert active_processes.exports[0].collection == "C000000001"
    assert active_processes.exports[0].project == "P000000001"
    assert active_processes.exports[0].project_title == "(UM) Test project #01"
    assert active_processes.exports[0].status == "in-queue-for-export"

    assert active_processes.unarchives[0].collection == "C000000001"
    assert active_processes.unarchives[0].project == "P000000001"
    assert active_processes.unarchives[0].project_title == "(UM) Test project #01"
    assert active_processes.unarchives[0].status == "unarchive-in-progress 1/1"

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
    "collection": "C000000001",
    "project": "P000000001",
    "project_title": "(UM) Test project #01",
    "repository": "SURFSara Tape",
    "state": "archive-in-progress 1/1",
    "title": "Title"
}
"""

ACTIVE_PROCESSES = """
{
    "archive": [
        {
            "collection": "C000000001",
            "project": "P000000001",
            "project_title": "(UM) Test project #01",
            "repository": "SURFSara Tape",
            "state": "archive-in-progress 1/1",
            "title": "Title"
        }
    ],
    "drop_zones": [
        {
            "creator": "jmelius",
            "date": "01675264813",
            "destination": "",
            "enableDropzoneSharing": "true",
            "project": "P000000001",
            "projectTitle": "(UM) Test project #01",
            "sharedWithMe": "true",
            "state": "open",
            "title": "Title",
            "token": "condemned-magpie",
            "totalSize": "0",
            "type": "direct",
            "validateMsg": "N/A",
            "validateState": "N/A"
        }
    ],
    "export": [
        {
            "collection": "C000000001",
            "project": "P000000001",
            "project_title": "(UM) Test project #01",
            "repository": "Dataverse",
            "state": "in-queue-for-export",
            "title": "Title"
        }
    ],
    "unarchive": [
        {
            "collection": "C000000001",
            "project": "P000000001",
            "project_title": "(UM) Test project #01",
            "repository": "SURFSara Tape",
            "state": "unarchive-in-progress 1/1",
            "title": "Title"
        }
    ]
}
"""