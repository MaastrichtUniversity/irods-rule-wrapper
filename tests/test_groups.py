from irodsrulewrapper.dto.group import Group
from irodsrulewrapper.dto.groups import Groups
from irodsrulewrapper.rule import RuleManager
import json


def test_rule_get_groups():
    result = RuleManager().get_groups("true")
    groups = result.groups
    assert groups is not None
    assert groups.__len__() >= 2
    assert groups[0].name is not None
    assert groups[0].id is not None
    assert groups[0].display_name is not None


def test_dto_group():
    group = Group.create_from_rule_result(json.loads(GROUP))
    assert group is not None
    assert group.name == "public"
    assert group.id == "10002"
    assert group.display_name == "public"


def test_dto_groups():
    result = Groups.create_from_rule_result(json.loads(GROUPS))
    assert result is not None
    assert result.groups.__len__() == 9
    assert result.groups[0].name == "datahub"
    assert result.groups[1].name == "public"


GROUP = '''
{
    "description": "",
    "displayName": "public",
    "userId": "10002",
    "userName": "public"
}
'''


GROUPS = '''
[
    {
        "description": "It's DataHub! The place to store your data.",
        "displayName": "DataHub",
        "userId": "10142",
        "userName": "datahub"
    },
    {
        "description": "",
        "displayName": "public",
        "userId": "10002",
        "userName": "public"
    },
    {
        "description": "",
        "displayName": "rodsadmin",
        "userId": "10001",
        "userName": "rodsadmin"
    },
    {
        "description": "",
        "displayName": "DH-project-admins",
        "userId": "10145",
        "userName": "DH-project-admins"
    },
    {
        "description": "CO for PhD project of P7000815",
        "displayName": "Novel approach for smashing ions",
        "userId": "10272",
        "userName": "m4i-nanoscopy-phd0815"
    },
    {
        "description": "",
        "displayName": "DH-ingest",
        "userId": "10025",
        "userName": "DH-ingest"
    },
    {
        "description": "UM-SCANNEXUS",
        "displayName": "SCANNEXUS",
        "userId": "10148",
        "userName": "scannexus"
    },
    {
        "description": "",
        "displayName": "m4i-massspec",
        "userId": "10265",
        "userName": "m4i-massspec"
    },
    {
        "description": "CO for all of nanoscopy",
        "displayName": "Nanoscopy",
        "userId": "10139",
        "userName": "m4i-nanoscopy"
    }
]
'''
