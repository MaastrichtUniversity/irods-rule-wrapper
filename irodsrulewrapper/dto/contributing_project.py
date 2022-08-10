"""This module contains the ContributingProject DTO class and its factory constructor."""
import json

from dhpythonirodsutils.enums import ProjectAVUs

from irodsrulewrapper.dto.groups import Groups
from irodsrulewrapper.dto.users import Users


class ContributingProject:
    """
    This class represents an iRODS project with its attributes and ACL, where the user has contributing access level.
    """

    def __init__(
        self,
        project_id: str,
        title: str,
        managers: Users,
        contributors_users: Users,
        contributors_groups: Groups,
        viewers_users: Users,
        viewers_groups: Groups,
        resource: str,
        collection_metadata_schemas,
    ):
        self.id: str = project_id
        self.title: str = title
        self.managers: Users = managers
        self.contributors_users: Users = contributors_users
        self.contributors_groups: Groups = contributors_groups
        self.viewers_users: Users = viewers_users
        self.viewers_groups: Groups = viewers_groups
        self.resource: str = resource
        self.collection_metadata_schemas = collection_metadata_schemas

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "ContributingProject":
        # get_contributing_project returns an empty list, if the user is not a contributor for the project
        if len(result) == 0:
            return None

        managers = Users.create_from_rule_result(result["managers"]["userObjects"])
        contributors_users = Users.create_from_rule_result(result["contributors"]["userObjects"])
        contributors_groups = Groups.create_from_rule_result(result["contributors"]["groupObjects"])
        viewers_users = Users.create_from_rule_result(result["viewers"]["userObjects"])
        viewers_groups = Groups.create_from_rule_result(result["viewers"]["groupObjects"])
        resource = result[ProjectAVUs.RESOURCE.value]
        project = cls(
            result["id"],
            result[ProjectAVUs.TITLE.value],
            managers,
            contributors_users,
            contributors_groups,
            viewers_users,
            viewers_groups,
            resource,
            result[ProjectAVUs.COLLECTION_METADATA_SCHEMAS.value],
        )

        return project

    @classmethod
    def create_from_mock_result(cls, mock_json=None) -> "ContributingProject":
        if mock_json is None:
            mock_json = CONTRIBUTING_PROJECT
        return ContributingProject.create_from_rule_result(json.loads(mock_json))


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
