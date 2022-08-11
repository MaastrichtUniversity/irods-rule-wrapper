"""This module contains the Projects DTO class, its factory constructors and mock_json."""
import json

from irodsrulewrapper.dto.project import Project


class Projects:
    """This class represents a list of iRODS Project DTOs."""

    def __init__(self, projects: list["Project"], has_financial_view_access: bool):
        self.projects: list["Project"] = projects
        self.has_financial_view_access: bool = has_financial_view_access

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "Projects":
        output = []
        for item in result["projects"]:
            project = Project.create_from_rule_result(item)
            output.append(project)
        projects = cls(output, result["has_financial_view_access"])
        return projects

    @classmethod
    def create_from_mock_result(cls, projects_json=None) -> "Projects":
        if projects_json is None:
            projects_json = cls.PROJECTS_JSON
        return Projects.create_from_rule_result(json.loads(projects_json))

    PROJECTS_JSON = """
    {
      "has_financial_view_access": true,
      "projects": [
        {
          "project": "test_project",
          "title": "test_title",
          "enableOpenAccessExport": false,
          "enableArchive": true,
          "enableUnarchive": true,
          "enableContributorEditMetadata": true,
          "enableDropzoneSharing": false,
          "principalInvestigatorDisplayName": "test_pi",
          "dataStewardDisplayName": "test_datasteward",
          "has_financial_view_access": true,
          "respCostCenter": "test_cost2",
          "storageQuotaGiB": 11,
          "dataSizeGiB": 99,
          "collectionMetadataSchemas": "test-schema-1,test-schema-2",
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
          "enableUnarchive": true,
          "enableContributorEditMetadata": true,
          "enableDropzoneSharing": false,
          "principalInvestigatorDisplayName": "test_pi2",
          "dataStewardDisplayName": "test_datasteward2",
          "has_financial_view_access": true,
          "respCostCenter": "test_cost2",
          "storageQuotaGiB": 11,
          "dataSizeGiB": 99,
          "collectionMetadataSchemas": "test-schema-1,test-schema-2",
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
    """
