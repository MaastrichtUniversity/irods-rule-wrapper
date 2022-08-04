from irodsrulewrapper.dto.groups import Groups, Group

import json


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
