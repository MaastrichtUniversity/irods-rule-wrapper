"""This module contains the Project DTO class, its factory constructors and mock_json."""
import json

from dhpythonirodsutils import formatters
from dhpythonirodsutils.enums import ProjectAVUs

from irodsrulewrapper.dto.groups import Groups
from irodsrulewrapper.dto.users import Users


class Project:
    """This class represents an iRODS project with its extended attributes and its ACL."""

    def __init__(
        self,
        project_id: str,
        title: str,
        description: str,
        enable_archive: bool,
        enable_unarchive: bool,
        enable_contributor_edit_metadata: bool,
        principal_investigator_display_name: str,
        data_steward_display_name: str,
        responsible_cost_center: str,
        storage_quota_gb: int,
        size: int,
        collection_metadata_schemas: str,
        enable_dropzone_sharing: bool,
        manager_users: Users,
        manager_groups: Groups,
        contributor_users: Users,
        contributor_groups: Groups,
        viewer_users: Users,
        viewer_groups: Groups,
        has_financial_view_access: bool,
    ):
        self.id: str = project_id
        self.title: str = title
        self.description: str = description
        self.enable_archive: bool = enable_archive
        self.enable_unarchive: bool = enable_unarchive
        self.enable_contributor_edit_metadata: bool = enable_contributor_edit_metadata
        self.principal_investigator_display_name: str = principal_investigator_display_name
        self.data_steward_display_name: str = data_steward_display_name
        self.responsible_cost_center: str = responsible_cost_center
        self.storage_quota_gb: int = storage_quota_gb
        self.size: int = size
        self.collection_metadata_schemas: str = collection_metadata_schemas
        self.enable_dropzone_sharing: bool = enable_dropzone_sharing
        self.manager_users: Users = manager_users
        self.manager_groups: Groups = manager_groups
        self.contributor_users: Users = contributor_users
        self.contributor_groups: Groups = contributor_groups
        self.viewer_users: Users = viewer_users
        self.viewer_groups: Groups = viewer_groups
        self.has_financial_view_access = has_financial_view_access

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "Project":
        if "principalInvestigatorDisplayName" not in result:
            result["principalInvestigatorDisplayName"] = ""
        if "dataStewardDisplayName" not in result:
            result["dataStewardDisplayName"] = ""
        project_details = cls(
            result["project"],
            result[ProjectAVUs.TITLE.value],
            result[ProjectAVUs.DESCRIPTION.value],
            formatters.format_string_to_boolean(result[ProjectAVUs.ENABLE_ARCHIVE.value]),
            formatters.format_string_to_boolean(result[ProjectAVUs.ENABLE_UNARCHIVE.value]),
            formatters.format_string_to_boolean(result[ProjectAVUs.ENABLE_CONTRIBUTOR_EDIT_METADATA.value]),
            result["principalInvestigatorDisplayName"],
            result["dataStewardDisplayName"],
            result["respCostCenter"],
            result["storageQuotaGiB"],
            result["dataSizeGiB"],
            result[ProjectAVUs.COLLECTION_METADATA_SCHEMAS.value],
            formatters.format_string_to_boolean(result[ProjectAVUs.ENABLE_DROPZONE_SHARING.value]),
            Users.create_from_rule_result(result["managers"]["userObjects"]),
            Groups.create_from_rule_result(result["managers"]["groupObjects"]),
            Users.create_from_rule_result(result["contributors"]["userObjects"]),
            Groups.create_from_rule_result(result["contributors"]["groupObjects"]),
            Users.create_from_rule_result(result["viewers"]["userObjects"]),
            Groups.create_from_rule_result(result["viewers"]["groupObjects"]),
            result["has_financial_view_access"],
        )
        return project_details

    @classmethod
    def create_from_mock_result(cls, project_json=None) -> "Project":
        if project_json is None:
            project_json = cls.PROJECT_JSON
        return Project.create_from_rule_result(json.loads(project_json))

    PROJECT_JSON = """
    {
        "project": "test_project",
        "title": "test_title",
        "description": "test_description",
        "enableArchive": true,
        "enableUnarchive": true,
        "enableContributorEditMetadata": true,
        "principalInvestigatorDisplayName": "test_pi",
        "dataStewardDisplayName": "test_datasteward",
        "respCostCenter": "test_cost2",
        "storageQuotaGiB": 11,
        "dataSizeGiB": 99,
        "collectionMetadataSchemas": ["test-schema-1", "test-schema-2"],
        "enableDropzoneSharing": false,
        "has_financial_view_access": true,
        "managers": {
            "userObjects":
            [
                {
                    "userName": "test_manager",
                    "displayName": "test_manager",
                    "userId": "0"
                }
            ],
            "groupObjects": [
                {
                    "groupName": "test_manager_group",
                    "groupId": "0",
                    "displayName": "Suppers en co",
                    "description": "some more details here"
                }
            ]
        },
        "contributors": {
            "userObjects":
            [
                {
                    "userName": "test_contributor",
                    "displayName": "test_contributor",
                    "userId": "1"
                }
            ],
            "groupObjects": [
                {
                    "groupName": "test_contributor_group",
                    "groupId": "1",
                    "displayName": "Suppers en co",
                    "description": "some more details here"
                }
            ]
        },
        "viewers": {
            "userObjects":
            [
                {
                    "userName": "test_viewer",
                    "displayName": "test_viewer",
                    "userId": "2"
                }
            ],
            "groupObjects": [
                {
                    "groupName": "test_viewer_group",
                    "groupId": "2",
                    "displayName": "Suppers en co",
                    "description": "some more details here"
                }
            ]
        }
    }
    """
