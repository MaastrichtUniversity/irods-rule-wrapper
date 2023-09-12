from irodsrulewrapper.dto.groups import Groups, Group

import json

from irodsrulewrapper.dto.users_groups_expanded import UsersGroupsExpanded


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


def test_dto_users_groups_extended():
    result = UsersGroupsExpanded.create_from_mock_result()
    user_groups = result
    assert user_groups is not None
    assert user_groups.__len__() == 10
    assert user_groups["auser"].display_name == "Additional User newly created in LDAP"
    assert user_groups["auser"].email == "auser"
    assert user_groups["jmelius"].display_name == "Jonathan M\u00e9lius"
    assert user_groups["jmelius"].email == "jmelius@um.nl"
    assert user_groups["datahub"].display_name == "DataHub"
    assert user_groups["datahub"].email == ""


GROUP = """
{
    "description": "",
    "displayName": "public",
    "userId": "10002",
    "userName": "public"
}
"""
