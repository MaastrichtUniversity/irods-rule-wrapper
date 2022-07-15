from irodsrulewrapper.dto.project import Project
from irodsrulewrapper.dto.project_contributors_metadata import ProjectContributorsMetadata
from irodsrulewrapper.dto.projects import Projects
from irodsrulewrapper.dto.projects_cost import ProjectsCost
from irodsrulewrapper.dto.managing_projects import ManagingProjects
from irodsrulewrapper.dto.projects_minimal import ProjectsMinimal


def test_dto_managing_projects():
    project = ManagingProjects.create_from_mock_result()
    assert project.managers == ["psuppers", "opalmen"]
    assert project.viewers == ["datahub"]


def test_dto_projects_cost():
    project = ProjectsCost.create_from_mock_result()
    assert project.projects_cost is not None


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


def test_dto_project_contributors_metadata():
    result = ProjectContributorsMetadata.create_from_mock_result()
    assert result is not None
    assert result.principal_investigator.display_name == "Pascal Suppers"
    assert result.data_steward.display_name == "Olav Palmen"


def test_dto_projects_minimal():
    projects = ProjectsMinimal.create_from_mock_result()
    assert projects.__len__() == 7
    assert projects[0].id == "P000000010"
    assert projects[0].title == "(MDL) Placeholder project"
    assert projects[1].title == "(HVC) Placeholder project"
    assert projects[6].id == "P000000016"
