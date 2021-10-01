from irodsrulewrapper.dto.data_stewards import DataStewards
from irodsrulewrapper.dto.data_steward import DataSteward
from irodsrulewrapper.rule import RuleManager
import json


def test_rule_get_data_stewards():
    result = RuleManager("rodsadmin").get_data_stewards()
    data_stewards = result.data_stewards
    assert data_stewards is not None
    assert data_stewards.__len__() >= 2
    assert data_stewards[0].user_name is not None
    assert data_stewards[0].user_id is not None
    assert data_stewards[0].display_name is not None


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
