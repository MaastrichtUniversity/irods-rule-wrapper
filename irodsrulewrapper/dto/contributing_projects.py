"""This module contains the ContributingProjects DTO class and its factory constructor."""
import json

from irodsrulewrapper.dto.contributing_project import ContributingProject


class ContributingProjects:
    """This class represents a list of iRODS ContributingProject DTOs."""

    def __init__(self, projects: list["ContributingProject"]):
        self.projects: list["ContributingProject"] = projects

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "ContributingProjects":
        # get_contributing_projects returns an empty list, if the user is not a contributor for the project
        if len(result) == 0:
            return None

        output = []
        for item in result:
            drop_zone = ContributingProject.create_from_rule_result(item)
            output.append(drop_zone)
        projects = cls(output)
        return projects

    @classmethod
    def create_from_mock_result(cls, mock_json=None) -> "ContributingProjects":
        if mock_json is None:
            mock_json = CONTRIBUTING_PROJECTS
        return ContributingProjects.create_from_rule_result(json.loads(mock_json))


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
