from .users import Users
from .groups import Groups
from typing import List, Dict


class Project:
    def __init__(self,
                 id: str,
                 title: str,
                 enable_open_access_export: bool,
                 enable_archive: bool,
                 enable_unarchive: bool,
                 principal_investigator_display_name: str,
                 data_steward_display_name: str,
                 responsible_cost_center: str,
                 storage_quota_gb: int,
                 size: int,
                 manager_users: Users,
                 manager_groups: Groups,
                 contributor_users: Users,
                 contributor_groups: Groups,
                 viewer_users: Users,
                 viewer_groups: Groups,
                 has_financial_view_access: bool):
        self.id: str = id
        self.title: str = title
        self.enable_open_access_export: bool = enable_open_access_export
        self.enable_archive: bool = enable_archive
        self.enable_unarchive: bool = enable_unarchive
        self.principal_investigator_display_name: str = principal_investigator_display_name
        self.data_steward_display_name: str = data_steward_display_name
        self.responsible_cost_center: str = responsible_cost_center
        self.storage_quota_gb: int = storage_quota_gb
        self.size: int = size
        self.manager_users: Users = manager_users
        self.manager_groups: Groups = manager_groups
        self.contributor_users: Users = contributor_users
        self.contributor_groups: Groups = contributor_groups
        self.viewer_users: Users = viewer_users
        self.viewer_groups: Groups = viewer_groups
        self.has_financial_view_access = has_financial_view_access

    @classmethod
    def create_from_rule_result(cls, result: Dict) -> 'Project':
        if "principalInvestigatorDisplayName" not in result:
            result["principalInvestigatorDisplayName"] = ''
        if "dataStewardDisplayName" not in result:
            result["dataStewardDisplayName"] = ''
        project_details = cls(result["project"],
                              result["title"],
                              result["enableOpenAccessExport"] == 'true',
                              result["enableArchive"] == 'true',
                              result["enableUnarchive"] == 'true',
                              result["principalInvestigatorDisplayName"],
                              result["dataStewardDisplayName"],
                              result["respCostCenter"],
                              result["storageQuotaGiB"],
                              result["dataSizeGiB"],
                              Users.create_from_rule_result(result['managers']['userObjects']),
                              Groups.create_from_rule_result(result['managers']['groupObjects']),
                              Users.create_from_rule_result(result['contributors']['userObjects']),
                              Groups.create_from_rule_result(result['contributors']['groupObjects']),
                              Users.create_from_rule_result(result['viewers']['userObjects']),
                              Groups.create_from_rule_result(result['viewers']['groupObjects']),
                              result["has_financial_view_access"])
        return project_details
