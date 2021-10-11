from irodsrulewrapper.dto.drop_zones import DropZones
from irodsrulewrapper.dto.drop_zone import DropZone
from irodsrulewrapper.rule import RuleManager


def test_rule_get_active_drop_zones():
    result = RuleManager(admin_mode=True).get_active_drop_zones("false")
    assert result is not None


def test_generate_token():
    result = RuleManager(admin_mode=True).generate_token()
    assert result is not None and result.token is not None


def test_rule_get_active_drop_zone():
    result = RuleManager(admin_mode=True).get_active_drop_zone("adorable-barracuda", "true")
    assert result is not None
