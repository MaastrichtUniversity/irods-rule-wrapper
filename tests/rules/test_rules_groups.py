from irodsrulewrapper.rule import RuleManager, RuleJSONManager


def test_rule_list_groups_users():
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
