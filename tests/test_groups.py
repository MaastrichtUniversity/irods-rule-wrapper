from irodsrulewrapper.dto.group import Group
from irodsrulewrapper.dto.groups import Groups
from irodsrulewrapper.rule import RuleManager, RuleJSONManager
import json


def test_rule_get_project_details_json():
    groups = RuleJSONManager(admin_mode=True).list_groups_users()
    assert groups is not None
    assert groups[0]["Users"] is not None


def test_rule_get_groups():
    result = RuleManager(admin_mode=True).get_groups("true")
    groups = result.groups
    assert groups is not None
    assert groups.__len__() >= 2
    assert groups[0].name is not None
    assert groups[0].id is not None
    assert groups[0].display_name is not None


def test_rule_get_users_in_group():
    result = RuleManager(admin_mode=True).get_users_in_group("10002")
    users = result.users
    assert users is not None
    assert users.__len__() >= 2
    assert users[0].user_name is not None
    assert users[0].user_id is not None
    assert users[0].display_name is not None


def test_dto_group():
    group = Group.create_from_rule_result(json.loads(GROUP))
    assert group is not None
    assert group.name == "public"
    assert group.id == "10002"
    assert group.display_name == "public"


def test_dto_groups():
    result = Groups.create_from_mock_result()
    groups = result.groups
    assert groups is not None
    assert groups.__len__() >= 2
    assert groups[0].name == "m4i-nanoscopy-phd0815"
    assert groups[0].id == "10199"
    assert groups[0].display_name == "Novel approach for smashing ions"
    assert groups[0].description == "CO for PhD project of P7000815"


GROUP = """
{
    "description": "",
    "displayName": "public",
    "userId": "10002",
    "userName": "public"
}
"""
