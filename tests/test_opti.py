# Note: Some of these tests require env variable CACHE_TTL_VALUE to be set
from irodsrulewrapper.rule import RuleManager


def test_rule_get_projects():
    result = RuleManager(admin_mode=True).get_projects("false")
    assert result is not None


def test_rule_get_projects_overview():
    result = RuleManager(admin_mode=True).get_projects_overview()
    assert result is not None


def test_rule_get_projects_overview_cached():
    result = RuleManager(admin_mode=True).get_projects_overview()
    assert result is not None


def test_rule_get_projects_overview_cached_ttl_reset():
    result = RuleManager(admin_mode=True).get_projects_overview()
    assert result is not None


def test_rule_get_projects_overview_cached_ttl_cached():
    result = RuleManager(admin_mode=True).get_projects_overview()
    assert result is not None


# def test_create_multiple_projects():
#     for x in range(100):
#         manager = RuleManager(admin_mode=True)
#         project = manager.create_new_project("authorizationPeriodEndDate", "dataRetentionPeriodEndDate",
#                                              "ingestResource", "resource", 42, "PyTest title", "jmelius",
#                                              "opalmen", "XXXXXXXXX", "true", "false")
#         assert project.project_id is not None
#         assert project.project_path is not None
#         # Set ACL otherwise list_project fails
#         manager.set_acl('default', 'own', "opalmen", project.project_path)
#         manager.set_acl('default', 'own', "jmelius", project.project_path)
