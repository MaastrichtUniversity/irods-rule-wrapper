from typing import List, Dict
from .users import User
from .groups import Group
from irodsrulewrapper.rule_managers.users import UserRuleManager


class ProjectOverview:
    def __init__(self,
                 id: str,
                 title: str,
                 enable_open_access_export: bool,
                 enable_archive: bool,
                 principal_investigator_display_name: str,
                 data_steward_display_name: str,
                 responsible_cost_center: str,
                 storage_quota_gb: int,
                 size: int,
                 manager_users: List,
                 contributor_users: List,
                 contributor_groups: List,
                 viewer_users: List,
                 viewer_groups: List,
                 has_financial_view_access: bool):
        self.id: str = id
        self.title: str = title
        self.enable_open_access_export: bool = enable_open_access_export
        self.enable_archive: bool = enable_archive
        self.principal_investigator_display_name: str = principal_investigator_display_name
        self.data_steward_display_name: str = data_steward_display_name
        self.responsible_cost_center: str = responsible_cost_center
        self.storage_quota_gb: int = storage_quota_gb
        self.size: int = size
        self.manager_users: List = manager_users
        self.contributor_users: List = contributor_users
        self.contributor_groups: List = contributor_groups
        self.viewer_users: List = viewer_users
        self.viewer_groups: List = viewer_groups
        self.has_financial_view_access = has_financial_view_access

    @classmethod
    def create_from_rule_result(cls, result: Dict) -> 'Project':

        if "enableOpenAccessExport" not in result:
            result["enableOpenAccessExport"] = False
        if "enableArchive" not in result:
            result["enableArchive"] = False

        manager_users = []
        contributor_users = []
        contributor_groups = []
        viewer_users = []
        viewer_groups = []

        for managers in result["managers"]:
            manager = UserRuleManager().get_user_or_group(managers)
            if isinstance(manager, User):
                manager_users.append(manager)

        for contributors in result["contributors"]:
            contributor = UserRuleManager().get_user_or_group(contributors)
            if isinstance(contributor, User):
                contributor_users.append(contributor)
            if isinstance(contributor, Group):
                contributor_groups.append(contributor)

        for viewers in result["viewers"]:
            viewer = UserRuleManager().get_user_or_group(viewers)
            if isinstance(viewer, User):
                viewer_users.append(viewer)
            if isinstance(viewer, Group):
                viewer_groups.append(viewer)

        project_details = cls(result["path"],
                              result["title"],
                              result["enableOpenAccessExport"] == 'true',
                              result["enableArchive"] == 'true',
                              result["OBI:0000103"],
                              result["dataSteward"],
                              result["responsibleCostCenter"],
                              result["storageQuotaGb"],
                              result["dataSizeGiB"],
                              manager_users,
                              contributor_users,
                              contributor_groups,
                              viewer_users,
                              viewer_groups,
                              False)
        #                              result["has_financial_view_access"]
        return project_details
