from irodsrulewrapper.dto.project import Project
from irodsrulewrapper.dto.projects import Projects
from irodsrulewrapper.dto.project_details import ProjectDetails
import json

PROJECT_JSON = '''
{
    "resource": "test_resource",
    "title": "test_title",
    "principalInvestigator": "test_pi",
    "respCostCenter": "test_cost",
    "storageQuotaGiB": 99,
    "dataSteward": "test_datasteward"
}
'''

PROJECTS_JSON = '''
[
{
    "resource": "test_resource",
    "title": "test_title",
    "principalInvestigator": "test_pi",
    "respCostCenter": "test_cost",
    "storageQuotaGiB": 99,
    "dataSteward": "test_datasteward"
},
{
    "resource": "test_resource2",
    "title": "test_title2",
    "principalInvestigator": "test_pi2",
    "respCostCenter": "test_cost2",
    "storageQuotaGiB": 11,
    "dataSteward": "test_datasteward2"
}
]
'''

PROJECT_DETAILS_JSON = '''
PLACEHOLDER
'''


def test_project():
    project = Project.create_from_rule_result(json.loads(PROJECT_JSON))
    assert project is not None
    assert project.resource == "test_resource"
    assert project.title == "test_title"
    assert project.pi == "test_pi"
    assert project.responsible_cost_center == "test_cost"
    assert project.storage_quota_gb == 99
    assert project.data_steward == "test_datasteward"


def test_projects():
    projects = Projects.create_from_rule_result(json.loads(PROJECTS_JSON))
    assert projects is not None
    assert projects.projects.__len__() == 2
    assert projects.projects[0].title == "test_title"
    assert projects.projects[1].title == "test_title2"


def test_project_details():
    project_details = ProjectDetails()
    assert project_details is not None
