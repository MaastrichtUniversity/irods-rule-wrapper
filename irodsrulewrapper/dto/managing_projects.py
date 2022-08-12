"""This module contains the ManagingProjects DTO class, its factory constructors and mock_json."""
import json

from irodsrulewrapper.dto.dto_base_model import DTOBaseModel


class ManagingProjects(DTOBaseModel):
    """
    This class represents an iRODS project with its attributes and ACL, where the user has managing access level.
    """

    managers: list[str]
    contributors: list[str]
    viewers: list[str]
    principal_investigator: str
    data_steward: str

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "ManagingProjects":
        # get_project_acl_for_manager returns an empty list, if the user is not a manager for the project
        if len(result) == 0:
            return None

        managers = result["managers"]["users"]
        contributors = result["contributors"]["users"] + result["contributors"]["groups"]
        viewers = result["viewers"]["users"] + result["viewers"]["groups"]
        projects = cls(
            managers=managers,
            contributors=contributors,
            viewers=viewers,
            principal_investigator=result["principal_investigator"],
            data_steward=result["data_steward"],
        )

        return projects

    @classmethod
    def create_from_mock_result(cls, mock_json=None) -> "ManagingProjects":
        if mock_json is None:
            mock_json = MOCK_JSON
        return cls.create_from_rule_result(json.loads(mock_json))


MOCK_JSON = """
{
  "principal_investigator": "psuppers",
  "managers": {
    "userObjects": [
      {
        "userName": "psuppers",
        "userId": "10058",
        "displayName": "psuppers"
      },
      {
        "userName": "opalmen",
        "userId": "10088",
        "displayName": "opalmen"
      }
    ],
    "users": [
      "psuppers",
      "opalmen"
    ],
    "groups": [],
    "groupObjects": []
  },
  "viewers": {
    "userObjects": [],
    "users": [],
    "groups": [
      "datahub"
    ],
    "groupObjects": [
      {
        "groupName": "datahub",
        "displayName": "datahub",
        "groupId": "10127",
        "description": ""
      }
    ]
  },
  "contributors": {
    "userObjects": [],
    "users": [],
    "groups": [],
    "groupObjects": []
  },
  "data_steward": "opalmen"
}
"""
