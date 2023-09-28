"""This module contains the ProjectOverview DTO class and its factory constructor."""
from dhpythonirodsutils.enums import ProjectAVUs

from irodsrulewrapper.convert_uid import convert_uids_to_users_or_groups


class ProjectOverview:
    """This class represents an iRODS project with a few of its attributes and its ACL."""

    def __init__(
        self,
        project_id: str,
        title: str,
        description: str,
        principal_investigator: str,
        data_steward: str,
        size: int,
        manager_users: list,
        contributor_users: list,
        contributor_groups: list,
        viewer_users: list,
        viewer_groups: list,
    ):
        self.id: str = project_id
        self.title: str = title
        self.description: str = description
        self.principal_investigator: str = principal_investigator
        self.data_steward: str = data_steward
        self.size: int = size
        self.manager_users: list = manager_users
        self.contributor_users: list = contributor_users
        self.contributor_groups: list = contributor_groups
        self.viewer_users: list = viewer_users
        self.viewer_groups: list = viewer_groups

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "ProjectOverview":
        user_groups = convert_uids_to_users_or_groups(result)

        if ProjectAVUs.DESCRIPTION.value not in result:
            result[ProjectAVUs.DESCRIPTION.value] = ""

        project_details = cls(
            result["path"],
            result[ProjectAVUs.TITLE.value],
            result[ProjectAVUs.DESCRIPTION.value],
            result[ProjectAVUs.PRINCIPAL_INVESTIGATOR.value],
            result[ProjectAVUs.DATA_STEWARD.value],
            result["dataSizeGiB"],
            user_groups.manager_users,
            user_groups.contributor_users,
            user_groups.contributor_groups,
            user_groups.viewer_users,
            user_groups.viewer_groups,
        )
        return project_details
