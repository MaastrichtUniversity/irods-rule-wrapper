from typing import List, Dict

from dhpythonirodsutils.enums import ProjectAVUs

from .users import User
from .groups import Group
from irodsrulewrapper.rule_managers.users import UserRuleManager


class ProjectOverview:
    def __init__(
        self,
        id: str,
        title: str,
        principal_investigator: str,
        data_steward: str,
        size: int,
        manager_users: List,
        contributor_users: List,
        contributor_groups: List,
        viewer_users: List,
        viewer_groups: List,
    ):
        self.id: str = id
        self.title: str = title
        self.principal_investigator: str = principal_investigator
        self.data_steward: str = data_steward
        self.size: int = size
        self.manager_users: List = manager_users
        self.contributor_users: List = contributor_users
        self.contributor_groups: List = contributor_groups
        self.viewer_users: List = viewer_users
        self.viewer_groups: List = viewer_groups

    @classmethod
    def create_from_rule_result(cls, result: Dict) -> "ProjectOverview":
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
            result["path"],
            result[ProjectAVUs.TITLE.value],
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
