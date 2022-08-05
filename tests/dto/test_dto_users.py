import json

from irodsrulewrapper.dto.data_stewards import DataStewards, DataSteward
from irodsrulewrapper.dto.user_extended import UserExtended
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
