import json

from irodsrulewrapper.dto.projects_overview import ProjectsOverview

from irodsrulewrapper.dto.project_contributors import ProjectContributors

from irodsrulewrapper.dto.contributing_project import ContributingProject
from irodsrulewrapper.dto.contributing_projects import ContributingProjects
from irodsrulewrapper.dto.create_project import CreateProject
from irodsrulewrapper.dto.managing_projects import ManagingProjects
from irodsrulewrapper.dto.migration_cards import MigrationCards, MigrationCard
from irodsrulewrapper.dto.project import Project
from irodsrulewrapper.dto.project_contributors_metadata import ProjectContributorsMetadata
from irodsrulewrapper.dto.projects import Projects
from irodsrulewrapper.dto.projects_cost import ProjectsCost
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


def test_dto_migration_card():
    card = MigrationCard.create_from_rule_result(json.loads(MIGRATION_CARD))
    assert card.status == "archive-done"
    assert card.repository == "SURFSara Tape"
    assert card.collection == "C000000001"
    assert card.title == "Test 1"


def test_dto_migration_cards():
    cards = MigrationCards.create_from_rule_result(json.loads(MIGRATION_CARDS)).cards
    assert cards[1].status == "in-queue-for-export"
    assert cards[1].repository == "DataverseNL"
    assert cards[1].collection == "C000000001"
    assert cards[1].title == "Test 1"


def test_dto_contributing_project():
    project = ContributingProject.create_from_rule_result(json.loads(CONTRIBUTING_PROJECT))
    assert project.id == "P000000014"
    assert project.title == "Hope that the day after you die is a nice day."
    assert project.managers.users[0].user_name == "psuppers"
    assert project.contributors_users.users == []
    assert project.contributors_groups.groups[0].name == ""
    assert project.contributors_groups.groups[0].display_name == "DataHub"
    assert project.viewers_users.users == []
    assert project.viewers_groups.groups == []
    assert project.resource == "replRescUM01"
    assert project.collection_metadata_schemas == "DataHub_general_schema,DataHub_extended_schema"


def test_dto_contributing_projects():
    projects = ContributingProjects.create_from_rule_result(json.loads(CONTRIBUTING_PROJECTS)).projects
    assert projects[1].id == "P000000015"
    assert projects[1].title == "Your society will be sought by people of taste and refinement."
    assert projects[1].managers.users[0].user_name == "psuppers"
    assert projects[1].contributors_users.users == []
    assert projects[1].contributors_groups.groups[0].name == ""
    assert projects[1].contributors_groups.groups[0].display_name == "DataHub"
    assert projects[1].viewers_users.users == []
    assert projects[1].viewers_groups.groups == []
    assert projects[1].resource == "replRescUM01"
    assert projects[1].collection_metadata_schemas == "DataHub_general_schema,DataHub_extended_schema"


def test_dto_create_project():
    result = CreateProject.create_from_rule_result(json.loads(CREATE_PROJECT))
    assert result.project_id == "P000000018"
    assert result.project_path == "/nlmumc/projects/P000000018"


def test_dto_project_contributors():
    project = ProjectContributors.create_from_rule_result(json.loads(PROJECT_CONTRIBUTORS))
    assert project.contributors_users == ["psuppers", "opalmen"]
    assert project.contributors_groups == ["datahub"]


# def test_dto_projects_overview():
#     projects = ProjectsOverview.create_from_rule_result(json.loads(PROJECTS_OVERVIEW)).projects
#     assert projects[3].id == "P000000015"
#     assert projects[3].title == "Your society will be sought by people of taste and refinement."
#     assert projects[3].principal_investigator == "psuppers"
#     assert projects[3].data_steward == "opalmen"
#     assert projects[3].size == 0.0
#     # assert projects[1].manager_users.users[0].user_name == "psuppers"
#     # assert projects[1].contributor_users.users == []
#     # assert projects[1].contributor_groups.groups[0].name == ""
#     # assert projects[1].contributor_groups.groups[0].display_name == "DataHub"
#     # assert projects[1].viewer_users.users == []
#     # assert projects[1].viewer_groups.groups == []
#
#     # manager_users: list,
#     # contributor_users: list,
#     # contributor_groups: list,
#     # viewer_users: list,
#     # viewer_groups: list,


MIGRATION_CARD = """
  {
    "status": "archive-done",
    "repository": "SURFSara Tape",
    "collection": "C000000001",
    "title": "Test 1"
  }
"""

MIGRATION_CARDS = """
[
  {
    "status": "archive-done",
    "repository": "SURFSara Tape",
    "collection": "C000000001",
    "title": "Test 1"
  },
  {
    "status": "in-queue-for-export",
    "repository": "DataverseNL",
    "collection": "C000000001",
    "title": "Test 1"
  }
]
"""

CONTRIBUTING_PROJECT = """
{
    "collectionMetadataSchemas": "DataHub_general_schema,DataHub_extended_schema",
    "contributors": {
        "groupObjects": [
            {
                "description": "It's DataHub! The place to store your data.",
                "displayName": "DataHub",
                "groupId": "10129",
                "groupName": "datahub"
            }
        ],
        "groups": [
            "datahub"
        ],
        "userObjects": [],
        "users": []
    },
    "id": "P000000014",
    "managers": {
        "groupObjects": [],
        "groups": [],
        "userObjects": [
            {
                "displayName": "Pascal Suppers",
                "userId": "10060",
                "userName": "psuppers"
            },
            {
                "displayName": "Olav Palmen",
                "userId": "10085",
                "userName": "opalmen"
            }
        ],
        "users": [
            "psuppers",
            "opalmen"
        ]
    },
    "resource": "replRescUM01",
    "title": "Hope that the day after you die is a nice day.",
    "viewers": {
        "groupObjects": [],
        "groups": [],
        "userObjects": [],
        "users": []
    }
}
"""

CONTRIBUTING_PROJECTS = """
[
    {
        "collectionMetadataSchemas": "DataHub_general_schema,DataHub_extended_schema",
        "contributors": {
            "groupObjects": [
                {
                    "description": "It's DataHub! The place to store your data.",
                    "displayName": "DataHub",
                    "groupId": "10129",
                    "groupName": "datahub"
                }
            ],
            "groups": [
                "datahub"
            ],
            "userObjects": [],
            "users": []
        },
        "id": "P000000014",
        "managers": {
            "groupObjects": [],
            "groups": [],
            "userObjects": [
                {
                    "displayName": "Pascal Suppers",
                    "userId": "10060",
                    "userName": "psuppers"
                },
                {
                    "displayName": "Olav Palmen",
                    "userId": "10085",
                    "userName": "opalmen"
                }
            ],
            "users": [
                "psuppers",
                "opalmen"
            ]
        },
        "resource": "replRescUM01",
        "title": "Hope that the day after you die is a nice day.",
        "viewers": {
            "groupObjects": [],
            "groups": [],
            "userObjects": [],
            "users": []
        }
    },
    {
        "collectionMetadataSchemas": "DataHub_general_schema,DataHub_extended_schema",
        "contributors": {
            "groupObjects": [
                {
                    "description": "It's DataHub! The place to store your data.",
                    "displayName": "DataHub",
                    "groupId": "10129",
                    "groupName": "datahub"
                }
            ],
            "groups": [
                "datahub"
            ],
            "userObjects": [],
            "users": []
        },
        "id": "P000000015",
        "managers": {
            "groupObjects": [],
            "groups": [],
            "userObjects": [
                {
                    "displayName": "Pascal Suppers",
                    "userId": "10060",
                    "userName": "psuppers"
                },
                {
                    "displayName": "Olav Palmen",
                    "userId": "10085",
                    "userName": "opalmen"
                }
            ],
            "users": [
                "psuppers",
                "opalmen"
            ]
        },
        "resource": "replRescUM01",
        "title": "Your society will be sought by people of taste and refinement.",
        "viewers": {
            "groupObjects": [],
            "groups": [],
            "userObjects": [],
            "users": []
        }
    }
]

"""

CREATE_PROJECT = """
{
    "project_id": "P000000018",
    "project_path": "/nlmumc/projects/P000000018"
}
"""

PROJECT_CONTRIBUTORS = """
{
    "groupObjects": [
        {
            "description": "It's DataHub! The place to store your data.",
            "displayName": "DataHub",
            "groupId": "10129",
            "groupName": "datahub"
        }
    ],
    "groups": [
        "datahub"
    ],
    "userObjects": [
            {
                "displayName": "Pascal Suppers",
                "userId": "10060",
                "userName": "psuppers"
            },
            {
                "displayName": "Olav Palmen",
                "userId": "10085",
                "userName": "opalmen"
            }
        ],
    "users": [
        "psuppers",
        "opalmen"
     ]
}
"""

PROJECTS_OVERVIEW = """
[
    {
        "OBI:0000103": "pvanschay2",
        "archiveDestinationResource": "arcRescSURF01",
        "authorizationPeriodEndDate": "1-1-2018",
        "collectionMetadataSchemas": "DataHub_general_schema,DataHub_extended_schema",
        "contributors": [
            "10126"
        ],
        "dataRetentionPeriodEndDate": "1-1-2018",
        "dataSizeGiB": 0.0,
        "dataSteward": "pvanschay2",
        "enableArchive": "true",
        "enableContributorEditMetadata": "false",
        "enableDropzoneSharing": "true",
        "enableOpenAccessExport": "false",
        "enableUnarchive": "true",
        "ingestResource": "iresResource",
        "managers": [
            "10055"
        ],
        "path": "P000000012",
        "resource": "replRescUM01",
        "responsibleCostCenter": "UM-12345678901B",
        "storageQuotaGb": "10",
        "title": "You recoil from the crude; you tend naturally toward the exquisite.",
        "viewers": []
    },
    {
        "OBI:0000103": "pvanschay2",
        "archiveDestinationResource": "arcRescSURF01",
        "authorizationPeriodEndDate": "1-1-2018",
        "collectionMetadataSchemas": "DataHub_general_schema,DataHub_extended_schema",
        "contributors": [
            "10126"
        ],
        "dataRetentionPeriodEndDate": "1-1-2018",
        "dataSizeGiB": 0.0,
        "dataSteward": "pvanschay2",
        "enableArchive": "true",
        "enableContributorEditMetadata": "false",
        "enableDropzoneSharing": "true",
        "enableOpenAccessExport": "false",
        "enableUnarchive": "true",
        "ingestResource": "iresResource",
        "managers": [
            "10055"
        ],
        "path": "P000000013",
        "resource": "replRescUM01",
        "responsibleCostCenter": "UM-12345678901B",
        "storageQuotaGb": "10",
        "title": "You will soon forget this.",
        "viewers": []
    },
    {
        "OBI:0000103": "psuppers",
        "archiveDestinationResource": "arcRescSURF01",
        "archiveState": "archive-done",
        "authorizationPeriodEndDate": "1-1-2018",
        "collectionMetadataSchemas": "DataHub_general_schema,DataHub_extended_schema",
        "contributors": [
            "10129"
        ],
        "dataRetentionPeriodEndDate": "1-1-2018",
        "dataSizeGiB": 0.9723356142640114,
        "dataSteward": "opalmen",
        "enableArchive": "true",
        "enableContributorEditMetadata": "false",
        "enableDropzoneSharing": "true",
        "enableOpenAccessExport": "true",
        "enableUnarchive": "true",
        "exporterState": "DataverseNL:in-queue-for-export",
        "ingestResource": "iresResource",
        "managers": [
            "10060",
            "10085"
        ],
        "path": "P000000014",
        "resource": "replRescUM01",
        "responsibleCostCenter": "UM-01234567890X",
        "storageQuotaGb": "10",
        "title": "Hope that the day after you die is a nice day.",
        "viewers": []
    },
    {
        "OBI:0000103": "psuppers",
        "archiveDestinationResource": "arcRescSURF01",
        "authorizationPeriodEndDate": "1-1-2018",
        "collectionMetadataSchemas": "DataHub_general_schema,DataHub_extended_schema",
        "contributors": [
            "10129"
        ],
        "dataRetentionPeriodEndDate": "1-1-2018",
        "dataSizeGiB": 0.0,
        "dataSteward": "opalmen",
        "enableArchive": "true",
        "enableContributorEditMetadata": "false",
        "enableDropzoneSharing": "true",
        "enableOpenAccessExport": "true",
        "enableUnarchive": "true",
        "ingestResource": "iresResource",
        "managers": [
            "10060",
            "10085"
        ],
        "path": "P000000015",
        "resource": "replRescUM01",
        "responsibleCostCenter": "UM-01234567890X",
        "storageQuotaGb": "10",
        "title": "Your society will be sought by people of taste and refinement.",
        "viewers": []
    }
]
"""
