from irodsrulewrapper.dto.user import User
from irodsrulewrapper.dto.users import Users
from irodsrulewrapper.rule import RuleManager
import json


def test_rule_get_username_attribute_value():
    result = RuleManager().get_username_attribute_value("jmelius", "eduPersonUniqueID")
    value = result.value
    assert value is not None
    assert value == "jmelius@sram.surf.nl"


def test_rule_get_user_group_memberships():
    result = RuleManager().get_user_group_memberships("true", "jmelius")
    assert result.groups is not None


def test_rule_get_users():
    result = RuleManager().get_users("true")
    users = result.users
    assert users is not None
    assert users.__len__() >= 2
    assert users[0].user_name is not None
    assert users[0].user_id is not None
    assert users[0].display_name is not None


def test_dto_user():
    user = User.create_from_rule_result(json.loads(PROJECT_USER))
    assert user is not None
    assert user.user_name == "jmelius"
    assert user.user_id == "10068"
    assert user.display_name == "Jonathan Melius"


def test_dto_users():
    result = Users.create_from_rule_result(json.loads(PROJECT_USERS))
    assert result is not None
    assert result.users.__len__() == 10
    assert result.users[0].user_name == "jmelius"
    assert result.users[1].user_name == "auser"


PROJECT_USER = '''
{
    "displayName": "Jonathan Melius",
    "userId": "10068",
    "userName": "jmelius"
}
'''

PROJECT_USERS = '''
[
    {
        "displayName": "Jonathan Melius",
        "userId": "10068",
        "userName": "jmelius"
    },
    {
        "displayName": "Additional User newly created in LDAP",
        "userId": "10113",
        "userName": "auser"
    },
    {
        "displayName": "Paul van Schayck",
        "userId": "10028",
        "userName": "pvanschay2"
    },
    {
        "displayName": "Maarten Coonen",
        "userId": "10038",
        "userName": "mcoonen"
    },
    {
        "displayName": "service-dropzones",
        "userId": "10123",
        "userName": "service-dropzones"
    },
    {
        "displayName": "Olav Palmen",
        "userId": "10098",
        "userName": "opalmen"
    },
    {
        "displayName": "Daniel Theunissen",
        "userId": "10048",
        "userName": "dtheuniss"
    },
    {
        "displayName": "Dr. Maarten Coonen (MUMC+)",
        "userId": "10043",
        "userName": "mcoonen2"
    },
    {
        "displayName": "Dean Linssen",
        "userId": "10118",
        "userName": "dlinssen"
    },
    {
        "displayName": "Pascal Suppers",
        "userId": "10053",
        "userName": "psuppers"
    }
]
'''
