"""This module contains the ContributingProject DTO class and its factory constructor."""
from dhpythonirodsutils.enums import ProjectAVUs

from irodsrulewrapper.dto.groups import Groups
from irodsrulewrapper.dto.users import Users

from pydantic import BaseModel


class ContributingProject(BaseModel):
    """
    This class represents an iRODS project with its attributes and ACL, where the user has contributing access level.
    """

    id: str
    title: str
    managers: Users
    contributors_users: Users
    contributors_groups: Groups
    viewers_users: Users
    viewers_groups: Groups
    resource: str
    collection_metadata_schemas: str

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
            id=result["id"],
            title=result[ProjectAVUs.TITLE.value],
            managers=managers,
            contributors_users=contributors_users,
            contributors_groups=contributors_groups,
            viewers_users=viewers_users,
            viewers_groups=viewers_groups,
            resource=resource,
            collection_metadata_schemas=result[ProjectAVUs.COLLECTION_METADATA_SCHEMAS.value],
        )

        return project
