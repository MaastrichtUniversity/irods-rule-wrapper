from irodsrulewrapper.dto.project import Project
from irodsrulewrapper.dto.projects import Projects
from irodsrulewrapper.dto.project_details import ProjectDetails

PROJECT_JSON = '''
PLACEHOLDER
'''

PROJECTS_JSON = '''
PLACEHOLDER
'''

PROJECT_DETAILS_JSON = '''

'''


def test_project():
    project = Project()
    assert project is not None


def test_projects():
    projects = Projects()
    assert projects is not None


def test_project_details():
    project_details = ProjectDetails()
    assert project_details is not None
