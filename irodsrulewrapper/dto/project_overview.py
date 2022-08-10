"""This module contains the ProjectOverview DTO class and its factory constructor."""
from dhpythonirodsutils.enums import ProjectAVUs
from pydantic import BaseModel

from irodsrulewrapper.dto.groups import Group
from irodsrulewrapper.dto.users import User
from irodsrulewrapper.rule_managers.users import UserRuleManager


class ProjectOverview(BaseModel):
    """This class represents an iRODS project with a few of its attributes and its ACL."""

    id: str
    title: str
    principal_investigator: str
    data_steward: str
    size: int
    manager_users: list[User]
    contributor_users: list[User]
    contributor_groups: list[Group]
    viewer_users: list[User]
    viewer_groups: list[Group]
    # def __init__(
    #     self,
    #     project_id: str,
    #     title: str,
    #     principal_investigator: str,
    #     data_steward: str,
    #     size: int,
    #     manager_users: list,
    #     contributor_users: list,
    #     contributor_groups: list,
    #     viewer_users: list,
    #     viewer_groups: list,
    # ):
    #     self.id: str = project_id
    #     self.title: str = title
    #     self.principal_investigator: str = principal_investigator
    #     self.data_steward: str = data_steward
    #     self.size: int = size
    #     self.manager_users: list = manager_users
    #     self.contributor_users: list = contributor_users
    #     self.contributor_groups: list = contributor_groups
    #     self.viewer_users: list = viewer_users
    #     self.viewer_groups: list = viewer_groups

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

        project_details = cls(
            id=result["path"],
            title=result[ProjectAVUs.TITLE.value],
            principal_investigator=result[ProjectAVUs.PRINCIPAL_INVESTIGATOR.value],
            data_steward=result[ProjectAVUs.DATA_STEWARD.value],
            size=result["dataSizeGiB"],
            manager_users=manager_users,
            contributor_users=contributor_users,
            contributor_groups=contributor_groups,
            viewer_users=viewer_users,
            viewer_groups=viewer_groups,
        )
        return project_details
