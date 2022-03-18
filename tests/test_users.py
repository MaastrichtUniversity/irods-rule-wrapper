from irodsrulewrapper.dto.user import User
from irodsrulewrapper.dto.user_extended import UserExtended
from irodsrulewrapper.dto.users import Users
from irodsrulewrapper.rule import RuleManager
import json


def test_rule_get_user_attribute_value():
    result = RuleManager(admin_mode=True).get_user_attribute_value("jmelius", "eduPersonUniqueID", "true")
    value = result.value
    assert value is not None
    assert value == "jmelius@sram.surf.nl"


def test_rule_set_username_attribute_value():
    RuleManager(admin_mode=True).set_username_attribute_value("jmelius", "lastToSAcceptedTimestamp", "1618476697")
    result = RuleManager(admin_mode=True).get_user_attribute_value("jmelius", "lastToSAcceptedTimestamp", "true")
    value = result.value
    assert value is not None
    assert value == "1618476697"


def test_rule_get_user_group_memberships():
    result = RuleManager(admin_mode=True).get_user_group_memberships("true", "jmelius")
    assert result.groups is not None


def test_rule_get_users():
    result = RuleManager(admin_mode=True).get_users("true")
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
