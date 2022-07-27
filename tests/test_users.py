import pytest

from irodsrulewrapper.dto.user import User
from irodsrulewrapper.dto.user_extended import UserExtended
from irodsrulewrapper.dto.users import Users
from irodsrulewrapper.rule import RuleManager
import json
import time

from irodsrulewrapper.utils import RuleInputValidationError


def test_rule_get_user_attribute_value():
    result = RuleManager(admin_mode=True).get_user_attribute_value("jmelius", "eduPersonUniqueID", "true")
    value = result.value
    assert value is not None
    assert value == "jmelius@sram.surf.nl"


def test_rule_set_username_attribute_value():
    RuleManager(admin_mode=True).set_user_attribute_value("jmelius", "lastToSAcceptedTimestamp", "1618476697")
    result = RuleManager(admin_mode=True).get_user_attribute_value("jmelius", "lastToSAcceptedTimestamp", "true")
    value = result.value
    assert value is not None
    assert value == "1618476697"


def test_rule_get_user_group_memberships():
    result = RuleManager(admin_mode=True).get_user_group_memberships("true", "jmelius")
    assert result.groups is not None


def test_rule_get_user_internal_affiliation_status():
    result = RuleManager(admin_mode=True).get_user_internal_affiliation_status("jmelius")
    is_internal = result.boolean
    assert is_internal is True
    result = RuleManager(admin_mode=True).get_user_internal_affiliation_status("auser")
    is_internal = result.boolean
    assert is_internal is False


def get_user_id_by_username(username):
    ret = RuleManager(admin_mode=True).get_users("false")
    for user in ret.users:
        if user.user_name == username:
            return int(user.user_id)
    return 10000


def test_count_user_temporary_passwords():
    user_id = get_user_id_by_username("jmelius")
    result = RuleManager(admin_mode=True).count_user_temporary_passwords(user_id)
    print(f"test result: {result}")


def test_get_user_temporary_password_creation_timestamp():
    user_id = get_user_id_by_username("jmelius")
    RuleManager(admin_mode=True).generate_temporary_password("jmelius", user_id)
    result = RuleManager(admin_mode=True).get_user_temporary_password_creation_timestamp(user_id)
    t = time.time()
    ts = int(result)
    assert isinstance(result, str)
    assert (ts - t) < 5

def test_generate_temporary_password_valid():
    user_id = get_user_id_by_username("jmelius")
    result = RuleManager(admin_mode=True).generate_temporary_password("jmelius",user_id)
    assert result['temporary_password'] is not None
    assert result['valid_until'] is not None

def test_generate_temporary_password_invalid_match():
    with pytest.raises(RuleInputValidationError) as e_info:
        result = RuleManager(admin_mode=True).generate_temporary_password("jmelius", 2000)
    assert str(e_info.value) == 'RuleInputValidationError, invalid match between *irods_user_name and *irods_id: expected a match'

def test_generate_temporary_password_invalid_account_type():
    with pytest.raises(RuleInputValidationError) as e_info:
        user_id = get_user_id_by_username("rods")
        result = RuleManager(admin_mode=True).generate_temporary_password("rods", user_id)
    assert str(e_info.value) == 'RuleInputValidationError, invalid irods user type for *irods_user_name: expected a rodsuser'

def test_generate_temporary_password_invalid_irods_id():
    with pytest.raises(RuleInputValidationError) as e_info:
        result = RuleManager(admin_mode=True).generate_temporary_password("rods", "test")
    assert str(e_info.value) == 'RuleInputValidationError, invalid type for *irods_id: expected a integer'


def test_remove_user_temporary_passwords():
    user_id = get_user_id_by_username("jmelius")
    RuleManager(admin_mode=True).remove_user_temporary_passwords(user_id)
    result = RuleManager(admin_mode=True).count_user_temporary_passwords(user_id)
    assert int(result) == 0


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
