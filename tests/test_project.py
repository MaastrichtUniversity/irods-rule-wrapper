from irodsrulewrapper.dto.project import Project
from irodsrulewrapper.dto.project_contributors_metadata import ProjectContributorsMetadata
from irodsrulewrapper.dto.projects import Projects
from irodsrulewrapper.dto.projects_cost import ProjectsCost
from irodsrulewrapper.dto.managing_projects import ManagingProjects
from irodsrulewrapper.rule import RuleManager, RuleJSONManager


def test_rule_details_project():
    project = RuleJSONManager(admin_mode=True).details_project("P000000011", "false")
    assert project is not None
    assert project["project"] is not None


def test_rule_list_projects_by_user():
    projects = RuleJSONManager(admin_mode=True).list_projects_by_user()
    assert projects is not None
    assert projects[0]["Projects"] is not None


def test_rule_get_project_details_json():
    project_details = RuleJSONManager(admin_mode=True).get_project_details("/nlmumc/projects/P000000011", "true")
    assert project_details is not None
    assert project_details["title"] == "(HVC) Placeholder project"


def test_rule_get_contributing_project_success():
    result = RuleManager("psuppers").get_contributing_project("P000000010", "false")
    assert result is not None


def test_rule_get_contributing_project_fail():
    # 'mcooonen' is in datahub group, and datahub group only has read permissions for P0..010
    result = RuleManager("mcoonen").get_contributing_project("P000000010", "false")
    assert result is None


def test_rule_get_project_contributors():
    result = RuleManager("opalmen").get_project_contributors("P000000010", "true", "false")
    assert result is not None


def test_rule_get_contributing_projects():
    result = RuleManager("jmelius").get_contributing_projects("false")
    assert result is not None


def test_rule_get_project_migration_status():
    result = RuleManager(admin_mode=True).get_project_migration_status("/nlmumc/projects/P000000010")
    cards = result.cards
    assert cards is not None


def test_rule_create_new_project():
    manager = RuleManager(admin_mode=True)
    project = manager.create_new_project(
        "ingestResource",
        "resource",
        "PyTest title",
        "jmelius",
        "opalmen",
        "XXXXXXXXX",
        {"enable_dropzone_sharing": "true"},
    )

    assert project.project_id is not None
    assert project.project_path is not None
    # Set ACL otherwise list_project fails
    manager.set_acl("default", "own", "opalmen", project.project_path)
    manager.set_acl("default", "own", "jmelius", project.project_path)


def test_rule_get_project_acl_for_manager():
    project = RuleManager("opalmen").get_project_acl_for_manager("P000000010", "false")
    assert project.viewers is not None
    assert project.contributors is not None
    assert project.managers is not None
    assert project.principal_investigator is not None
    assert project.data_steward is not None


def test_json_get_project_acl_for_manager():
    project = RuleJSONManager("opalmen").get_project_acl_for_manager("P000000010", "false")
    assert project is not None


def test_dto_managing_projects():
    project = ManagingProjects.create_from_mock_result()
    assert project.managers == ["psuppers", "opalmen"]
    assert project.viewers == ["datahub"]


def test_rule_get_projects_finance():
    project = RuleManager("opalmen").get_projects_finance()
    assert project.projects_cost is not None


def test_dto_projects_cost():
    project = ProjectsCost.create_from_mock_result()
    assert project.projects_cost is not None


def test_rule_get_project_details():
    project_details = RuleManager(admin_mode=True).get_project_details("/nlmumc/projects/P000000011", "true")
    assert project_details is not None
    assert project_details.principal_investigator_display_name == "Pascal Suppers"
    assert project_details.data_steward_display_name == "Olav Palmen"
    assert project_details.responsible_cost_center == "AZM-123456"
    assert project_details.manager_users.users[0].display_name == "Pascal Suppers"
    assert project_details.contributor_users.users[0].display_name == "service-mdl"
    # assert project_details.viewer_groups.groups[0].display_name == 'DataHub'
    assert project_details.title == "(HVC) Placeholder project"
    assert project_details.enable_open_access_export is False
    assert project_details.enable_archive is False
    assert project_details.has_financial_view_access is False
    assert project_details.size == 0


def test_rule_get_projects():
    result = RuleManager(admin_mode=True).get_projects("false")
    projects = result.projects
    assert projects is not None
    assert projects.__len__() >= 2
    assert projects[0].title == "(MDL) Placeholder project"
    assert projects[1].title == "(HVC) Placeholder project"


def test_dto_project():
    project_details = Project.create_from_mock_result()
    assert project_details is not None
    assert project_details.manager_users.users[0].display_name == "test_manager"
    assert project_details.contributor_users.users[0].display_name == "test_contributor"
    assert project_details.viewer_users.users[0].display_name == "test_viewer"
    assert project_details.title == "test_title"
    assert project_details.enable_open_access_export is False
    assert project_details.enable_archive is False
    assert project_details.has_financial_view_access is True
    assert project_details.size == 99


def test_dto_projects():
    projects = Projects.create_from_mock_result()
    assert projects is not None
    assert projects.projects.__len__() == 2
    assert projects.projects[0].title == "test_title"
    assert projects.projects[1].title == "test_title2"


def test_rule_get_project_contributors_metadata():
    result = RuleManager(admin_mode=True).get_project_contributors_metadata("P000000011")
    assert result is not None
    assert result.principal_investigator.display_name == "Pascal Suppers"
    assert result.data_steward.display_name == "Olav Palmen"


def test_dto_project_contributors_metadata():
    result = ProjectContributorsMetadata.create_from_mock_result()
    assert result is not None
    assert result.principal_investigator.display_name == "Pascal Suppers"
    assert result.data_steward.display_name == "Olav Palmen"
