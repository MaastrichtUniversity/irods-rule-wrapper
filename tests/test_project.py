from irodsrulewrapper.dto.project import Project
from irodsrulewrapper.dto.projects import Projects
import json




def test_project():
    project_details = Project.create_from_rule_result(json.loads(PROJECT_JSON))
    assert project_details is not None
    assert project_details.manager_users.users[0].display_name == 'test_manager'
    assert project_details.contributor_users.users[0].display_name == 'test_contributor'
    assert project_details.viewer_users.users[0].display_name == 'test_viewer'
    assert project_details.title == 'test_title'
    assert project_details.enable_open_access_export is False
    assert project_details.enable_archive is True
    assert project_details.size == 99


def test_projects():
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
[
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
},
{
    "project": "test_project2",
    "title": "test_title2",
    "enableOpenAccessExport": false,
    "enableArchive": true,
    "principalInvestigatorDisplayName": "test_pi2",
    "dataStewardDisplayName": "test_datasteward2",
    "respCostCenter": "test_cost2",
    "storageQuotaGiB": 11,
    "dataSizeGiB": 99,
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
]
'''


