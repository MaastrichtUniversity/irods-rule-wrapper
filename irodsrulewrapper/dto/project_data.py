from .users import Users
from .groups import Groups
from typing import List, Dict


class ProjectData:
    def __init__(self,
                 project: str,
                 title: str,
                 enable_open_access_export: bool,
                 enable_archive: bool,
                 principal_investigator_display_name: str,
                 data_steward_display_name: str,
                 manager_users: Users,
                 manager_groups: Users,
                 contributor_users: Users,
                 contributor_groups: Groups,
                 viewer_users: Users,
                 viewer_groups: Groups):
        self.project: str = project
        self.title: str = title
        self.enable_open_access_export: bool = enable_open_access_export
        self.enable_archive: bool = enable_archive
        self.principal_investigator_display_name: str = principal_investigator_display_name
        self.data_steward_display_name: str = data_steward_display_name
        self.manager_users: Users = manager_users
        self.manager_groups: Groups = manager_groups
        self.contributor_users: Users = contributor_users
        self.contributor_groups: Groups = contributor_groups
        self.viewer_users: Users = viewer_users
        self.viewer_groups: Groups = viewer_groups

    @classmethod
    def create_from_rule_result(cls, result: Dict) -> 'ProjectData':
        project_details = cls(result["project"],
                              result["title"],
                              result["enableOpenAccessExport"],
                              result["enableArchive"],
                              result["principalInvestigatorDisplayName"],
                              result["dataStewardDisplayName"],
                              Users.create_from_rule_result(result['managers']['userObjects']),
                              Groups.create_from_rule_result(result['managers']['groupObjects']),
                              Users.create_from_rule_result(result['contributors']['userObjects']),
                              Groups.create_from_rule_result(result['contributors']['groupObjects']),
                              Users.create_from_rule_result(result['viewers']['userObjects']),
                              Groups.create_from_rule_result(result['viewers']['groupObjects']))
        return project_details
