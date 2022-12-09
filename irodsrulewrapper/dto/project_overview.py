"""This module contains the ProjectOverview DTO class and its factory constructor."""
from dhpythonirodsutils.enums import ProjectAVUs

from irodsrulewrapper.dto.groups import Group
from irodsrulewrapper.dto.users import User
from irodsrulewrapper.rule_managers.users import UserRuleManager


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
        manager_users = []
        contributor_users = []
        contributor_groups = []
        viewer_users = []
        viewer_groups = []

        rule_manager = UserRuleManager(admin_mode=True)
        for managers in result["managers"]:
            manager = rule_manager.get_user_or_group(managers)
            if isinstance(manager, User):
                manager_users.append(manager)

        for contributors in result["contributors"]:
            contributor = rule_manager.get_user_or_group(contributors)
            if isinstance(contributor, User):
                contributor_users.append(contributor)
            elif isinstance(contributor, Group):
                contributor_groups.append(contributor)

        for viewers in result["viewers"]:
            viewer = rule_manager.get_user_or_group(viewers)
            if isinstance(viewer, User):
                viewer_users.append(viewer)
            elif isinstance(viewer, Group):
                viewer_groups.append(viewer)

        if ProjectAVUs.DESCRIPTION.value not in result:
            result[ProjectAVUs.DESCRIPTION.value] = ""

        project_details = cls(
            result["path"],
            result[ProjectAVUs.TITLE.value],
            result[ProjectAVUs.DESCRIPTION.value],
            result[ProjectAVUs.PRINCIPAL_INVESTIGATOR.value],
            result[ProjectAVUs.DATA_STEWARD.value],
            result["dataSizeGiB"],
            manager_users,
            contributor_users,
            contributor_groups,
            viewer_users,
            viewer_groups,
        )
        return project_details
