from irodsrulewrapper.rule import RuleManager
import pytest

def test_rule_get_active_drop_zones():
    result = RuleManager(admin_mode=True).get_active_drop_zones("false")
    assert result is not None


def test_generate_token():
    result = RuleManager(admin_mode=True).generate_token()
    assert result is not None and result.token is not None


# never been tested, original two below
@pytest.mark.skip(reason="excluded from overall testing because these need specific setup.")
def test_rule_get_active_drop_zone_mounted():
    result = RuleManager(admin_mode=True).get_active_drop_zone("adorable-barracuda", "true", "mounted")
    assert result is not None


# never been tested, original below
@pytest.mark.skip(reason="excluded from overall testing because these need specific setup.")
def test_rule_get_active_drop_zone_direct():
    result = RuleManager(admin_mode=True).get_active_drop_zone("adorable-barracuda", "true", "direct")
    assert result is not None

# def test_rule_get_active_drop_zone():
#     result = RuleManager(admin_mode=True).get_active_drop_zone("adorable-barracuda", "true")
#     assert result is not None
