from irodsrulewrapper.dto.project import Project
from irodsrulewrapper.dto.projects import Projects
from irodsrulewrapper.rule import RuleManager
import json


def test_rule_get_contributing_projects():
    result = RuleManager('jmelius').get_contributing_projects()
    assert result is not None


def test_rule_create_new_project():
    manager = RuleManager()
    project = manager.create_new_project("authorizationPeriodEndDate", "dataRetentionPeriodEndDate",
                       "ingestResource", "resource", 42, "PyTest title", "jmelius",
                       "opalmen", "XXXXXXXXX", "true", "false")
    assert project.project_id is not None
    assert project.project_path is not None
    # Set ACL otherwise list_project fails
    manager.set_acl('default', 'own', "opalmen", project.project_path)
    manager.set_acl('default', 'own', "jmelius", project.project_path)


def test_rule_get_managing_project():
    project = RuleManager('opalmen').get_managing_project('P000000010')
    assert project.viewers is not None
    assert project.contributors is not None
    assert project.managers is not None
    assert project.principal_investigator is not None
    assert project.data_steward is not None


def test_rule_get_projects_finance():
    project = RuleManager('jmelius').get_projects_finance()
    assert project.projects_cost is not None


def test_rule_get_project_details():
    project_details = RuleManager().get_project_details("/nlmumc/projects/P000000011")
    assert project_details is not None
    assert project_details.principal_investigator_display_name == "Pascal Suppers"
    assert project_details.data_steward_display_name == "Olav Palmen"
    assert project_details.responsible_cost_center == "AZM-123456"
    assert project_details.manager_users.users[0].display_name == 'Pascal Suppers'
    assert project_details.contributor_users.users[0].display_name == 'service-mdl'
    # assert project_details.viewer_groups.groups[0].display_name == 'DataHub'
    assert project_details.title == '(HVC) Placeholder project'
    assert project_details.enable_open_access_export is False
    assert project_details.enable_archive is False
    assert project_details.has_financial_view_access is False
    assert project_details.size == 0


def test_rule_get_projects():
    result = RuleManager().get_projects()
    projects = result.projects
    assert projects is not None
    assert projects.__len__() >= 2
    assert projects[0].title == "(MDL) Placeholder project"
    assert projects[1].title == '(HVC) Placeholder project'


def test_dto_project():
    project_details = Project.create_from_rule_result(json.loads(PROJECT_JSON))
    assert project_details is not None
    assert project_details.manager_users.users[0].display_name == 'test_manager'
    assert project_details.contributor_users.users[0].display_name == 'test_contributor'
    assert project_details.viewer_users.users[0].display_name == 'test_viewer'
    assert project_details.title == 'test_title'
    assert project_details.enable_open_access_export is False
    assert project_details.enable_archive is False
    assert project_details.has_financial_view_access is True
    assert project_details.size == 99


def test_dto_projects():
    projects = Projects.create_from_rule_result(json.loads(PROJECTS_JSON))
    assert projects is not None
    assert projects.projects.__len__() == 2
    assert projects.projects[0].title == "test_title"
    assert projects.projects[1].title == "test_title2"


PROJECT_JSON = '''
{
    "project": "test_project",
    "title": "test_title",
    "enableOpenAccessExport": false,
    "enableArchive": true,
    "principalInvestigatorDisplayName": "test_pi",
    "dataStewardDisplayName": "test_datasteward",
    "respCostCenter": "test_cost2",
    "storageQuotaGiB": 11,
    "dataSizeGiB": 99,
    "has_financial_view_access": true,
    "managers": {
        "userObjects":
        [
            {
                "userName": "test_manager",
                "displayName": "test_manager",
                "userId": "0"
            }
        ],
        "groupObjects": [
            {
                "groupName": "test_manager_group",
                "groupId": "0",
                "displayName": "Suppers en co",
                "description": "some more details here"
            }
        ]
    },
    "contributors": {
        "userObjects":
        [
            {
                "userName": "test_contributor",
                "displayName": "test_contributor",
                "userId": "1"
            }
        ],
        "groupObjects": [
            {
                "groupName": "test_contributor_group",
                "groupId": "1",
                "displayName": "Suppers en co",
                "description": "some more details here"
            }
        ]
    },
    "viewers": {
        "userObjects":
        [
            {
                "userName": "test_viewer",
                "displayName": "test_viewer",
                "userId": "2"
            }
        ],
        "groupObjects": [
            {
                "groupName": "test_viewer_group",
                "groupId": "2",
                "displayName": "Suppers en co",
                "description": "some more details here"
            }
        ]
    }
}
'''

PROJECTS_JSON = '''
{
  "has_financial_view_access": true,
  "projects": [
    {
      "project": "test_project",
      "title": "test_title",
      "enableOpenAccessExport": false,
      "enableArchive": true,
      "principalInvestigatorDisplayName": "test_pi",
      "dataStewardDisplayName": "test_datasteward",
      "has_financial_view_access": true,
      "respCostCenter": "test_cost2",
      "storageQuotaGiB": 11,
      "dataSizeGiB": 99,
      "managers": {
        "userObjects": [
          {
            "userName": "test_manager",
            "displayName": "test_manager",
            "userId": "0"
          }
        ],
        "groupObjects": [
          {
            "groupName": "test_manager_group",
            "groupId": "0",
            "displayName": "Suppers en co",
            "description": "some more details here"
          }
        ]
      },
      "contributors": {
        "userObjects": [
          {
            "userName": "test_contributor",
            "displayName": "test_contributor",
            "userId": "1"
          }
        ],
        "groupObjects": [
          {
            "groupName": "test_contributor_group",
            "groupId": "1",
            "displayName": "Suppers en co",
            "description": "some more details here"
          }
        ]
      },
      "viewers": {
        "userObjects": [
          {
            "userName": "test_viewer",
            "displayName": "test_viewer",
            "userId": "2"
          }
        ],
        "groupObjects": [
          {
            "groupName": "test_viewer_group",
            "groupId": "2",
            "displayName": "Suppers en co",
            "description": "some more details here"
          }
        ]
      }
    },
    {
      "project": "test_project2",
      "title": "test_title2",
      "enableOpenAccessExport": false,
      "enableArchive": true,
      "principalInvestigatorDisplayName": "test_pi2",
      "dataStewardDisplayName": "test_datasteward2",
      "has_financial_view_access": true,
      "respCostCenter": "test_cost2",
      "storageQuotaGiB": 11,
      "dataSizeGiB": 99,
      "managers": {
        "userObjects": [
          {
            "userName": "test_manager",
            "displayName": "test_manager",
            "userId": "0"
          }
        ],
        "groupObjects": [
          {
            "groupName": "test_manager_group",
            "groupId": "0",
            "displayName": "Suppers en co",
            "description": "some more details here"
          }
        ]
      },
      "contributors": {
        "userObjects": [
          {
            "userName": "test_contributor",
            "displayName": "test_contributor",
            "userId": "1"
          }
        ],
        "groupObjects": [
          {
            "groupName": "test_contributor_group",
            "groupId": "1",
            "displayName": "Suppers en co",
            "description": "some more details here"
          }
        ]
      },
      "viewers": {
        "userObjects": [
          {
            "userName": "test_viewer",
            "displayName": "test_viewer",
            "userId": "2"
          }
        ],
        "groupObjects": [
          {
            "groupName": "test_viewer_group",
            "groupId": "2",
            "displayName": "Suppers en co",
            "description": "some more details here"
          }
        ]
      }
    }
  ]
}
'''


