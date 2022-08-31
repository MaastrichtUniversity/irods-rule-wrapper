import time

import pytest

from irodsrulewrapper.rule import RuleManager, RuleJSONManager
from irodsrulewrapper.utils import RuleInputValidationError


# region users rules


def test_rule_get_users():
    result = RuleManager(admin_mode=True).get_users("true")
    users = result.users
    assert users is not None
    assert users.__len__() >= 2
    assert users[0].user_name is not None
    assert users[0].user_id is not None
    assert users[0].display_name is not None


def test_rule_get_data_stewards():
    result = RuleManager(admin_mode=True).get_data_stewards()
    data_stewards = result.data_stewards
    assert data_stewards is not None
    assert data_stewards.__len__() >= 2
    assert data_stewards[0].user_name is not None
    assert data_stewards[0].user_id is not None
    assert data_stewards[0].display_name is not None


def test_rule_get_user_attribute_value():
    result = RuleManager(admin_mode=True).get_user_attribute_value("jmelius", "eduPersonUniqueID", "true")
    value = result.value
    assert value is not None
    assert value == "jmelius@sram.surf.nl"


def test_rule_set_user_attribute_value():
    RuleManager(admin_mode=True).set_user_attribute_value("jmelius", "lastToSAcceptedTimestamp", "1618476697")
    result = RuleManager(admin_mode=True).get_user_attribute_value("jmelius", "lastToSAcceptedTimestamp", "true")
    value = result.value
    assert value is not None
    assert value == "1618476697"


def test_rule_get_user_internal_affiliation_status():
    result = RuleManager(admin_mode=True).get_user_internal_affiliation_status("jmelius")
    is_internal = result.boolean
    assert is_internal is True
    result = RuleManager(admin_mode=True).get_user_internal_affiliation_status("auser")
    is_internal = result.boolean
    assert is_internal is False


def test_get_user_or_group_by_id():
    rule_manager = RuleManager(admin_mode=True)
    user_id = rule_manager.get_irods_user_id_by_username("jmelius")
    result = rule_manager.get_user_or_group_by_id(str(user_id))
    assert result is not None


def test_get_user_or_group():
    rule_manager = RuleManager(admin_mode=True)
    user_id = rule_manager.get_irods_user_id_by_username("jmelius")
    user = rule_manager.get_user_or_group(str(user_id))
    assert user is not None
    assert user.user_name == "jmelius"
    assert user.user_id == str(user_id)


# endregion

# region temporary password


def test_get_temporary_password_lifetime():
    ttl = RuleJSONManager(admin_mode=True).get_temporary_password_lifetime()
    assert ttl >= 0


def test_count_user_temporary_passwords():
    rule_manager = RuleJSONManager(admin_mode=True)
    user_id = rule_manager.get_irods_user_id_by_username("jmelius")
    result = rule_manager.count_user_temporary_passwords(user_id)
    rule_manager.session.cleanup()
    assert result is not None


def test_get_user_temporary_password_creation_timestamp():
    rule_manager = RuleJSONManager(admin_mode=True)
    user_id = rule_manager.get_irods_user_id_by_username("jmelius")
    rule_manager.generate_temporary_password("jmelius", user_id)
    time_stamp = rule_manager.get_user_temporary_password_creation_timestamp(user_id)
    rule_manager.session.cleanup()
    # Check if the timestamp of the generated temp password is within 5 seconds of the current time
    t = time.time()
    assert isinstance(time_stamp, int)
    assert (time_stamp - t) < 5


def test_generate_temporary_password_valid():
    rule_manager = RuleJSONManager(admin_mode=True)
    user_id = rule_manager.get_irods_user_id_by_username("jmelius")
    result = rule_manager.generate_temporary_password("jmelius", user_id)
    rule_manager.session.cleanup()
    assert result["temporary_password"] is not None
    assert result["valid_until"] is not None


def test_generate_temporary_password_invalid_match():
    rule_manager = RuleJSONManager(admin_mode=True)
    with pytest.raises(RuleInputValidationError) as e_info:
        rule_manager.generate_temporary_password("jmelius", 2000)
    rule_manager.session.cleanup()
    assert (
        str(e_info.value)
        == "RuleInputValidationError, invalid match between *irods_user_name and *irods_id: expected a match"
    )


def test_generate_temporary_password_invalid_account_type():
    rule_manager = RuleJSONManager(admin_mode=True)
    user_id = rule_manager.get_irods_user_id_by_username("rods")
    with pytest.raises(RuleInputValidationError) as e_info:
        rule_manager.generate_temporary_password("rods", user_id)
    rule_manager.session.cleanup()
    assert (
        str(e_info.value)
        == "RuleInputValidationError, invalid irods user type for *irods_user_name: expected a rodsuser"
    )


def test_generate_temporary_password_invalid_irods_id():
    with pytest.raises(RuleInputValidationError) as e_info:
        RuleJSONManager(admin_mode=True).generate_temporary_password("rods", "test")
    assert str(e_info.value) == "RuleInputValidationError, invalid type for *irods_id: expected a integer"


def test_remove_user_temporary_passwords():
    rule_manager = RuleJSONManager(admin_mode=True)
    user_id = rule_manager.get_irods_user_id_by_username("jmelius")
    rule_manager.remove_user_temporary_passwords(user_id)
    result = rule_manager.count_user_temporary_passwords(user_id)
    rule_manager.session.cleanup()
    assert result == 0


# endregion
