"""This module contains the Project DTO class, its factory constructors and mock_json."""
import json

from dhpythonirodsutils import formatters
from dhpythonirodsutils.enums import ProjectAVUs

from irodsrulewrapper.dto.dto_base_model import DTOBaseModel
from irodsrulewrapper.dto.groups import Groups
from irodsrulewrapper.dto.users import Users


class Project(DTOBaseModel):
    """This class represents an iRODS project with its extended attributes and its ACL."""

    id: str
    title: str
    enable_open_access_export: bool
    enable_archive: bool
    enable_unarchive: bool
    enable_contributor_edit_metadata: bool
    principal_investigator_display_name: str
    data_steward_display_name: str
    responsible_cost_center: str
    storage_quota_gb: int
    size: int
    collection_metadata_schemas: str
    enable_dropzone_sharing: bool
    manager_users: Users
    contributor_users: Users
    contributor_groups: Groups
    viewer_users: Users
    viewer_groups: Groups
    has_financial_view_access: bool

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "Project":
        if "principalInvestigatorDisplayName" not in result:
            result["principalInvestigatorDisplayName"] = ""
        if "dataStewardDisplayName" not in result:
            result["dataStewardDisplayName"] = ""
        project_details = cls(
            id=result["project"],
            title=result[ProjectAVUs.TITLE.value],
            enable_open_access_export=formatters.format_string_to_boolean(
                result[ProjectAVUs.ENABLE_OPEN_ACCESS_EXPORT.value]
            ),
            enable_archive=formatters.format_string_to_boolean(result[ProjectAVUs.ENABLE_ARCHIVE.value]),
            enable_unarchive=formatters.format_string_to_boolean(result[ProjectAVUs.ENABLE_UNARCHIVE.value]),
            enable_contributor_edit_metadata=formatters.format_string_to_boolean(
                result[ProjectAVUs.ENABLE_CONTRIBUTOR_EDIT_METADATA.value]
            ),
            principal_investigator_display_name=result["principalInvestigatorDisplayName"],
            data_steward_display_name=result["dataStewardDisplayName"],
            responsible_cost_center=result["respCostCenter"],
            storage_quota_gb=result["storageQuotaGiB"],
            size=result["dataSizeGiB"],
            collection_metadata_schemas=result[ProjectAVUs.COLLECTION_METADATA_SCHEMAS.value],
            enable_dropzone_sharing=formatters.format_string_to_boolean(
                result[ProjectAVUs.ENABLE_DROPZONE_SHARING.value]
            ),
            manager_users=Users.create_from_rule_result(result["managers"]["userObjects"]),
            contributor_users=Users.create_from_rule_result(result["contributors"]["userObjects"]),
            contributor_groups=Groups.create_from_rule_result(result["contributors"]["groupObjects"]),
            viewer_users=Users.create_from_rule_result(result["viewers"]["userObjects"]),
            viewer_groups=Groups.create_from_rule_result(result["viewers"]["groupObjects"]),
            has_financial_view_access=result["has_financial_view_access"],
        )
        return project_details

    @classmethod
    def create_from_mock_result(cls, mock_json=None) -> "Project":
        if mock_json is None:
            mock_json = PROJECT_JSON
        return Project.create_from_rule_result(json.loads(mock_json))


PROJECT_JSON = """
    {
        "project": "P000000015",
        "title": "test title",
        "enableOpenAccessExport": false,
        "enableArchive": true,
        "enableUnarchive": true,
        "enableContributorEditMetadata": true,
        "principalInvestigatorDisplayName": "Pascal Suppers",
        "dataStewardDisplayName": "Olav Palmen",
        "respCostCenter": "test_cost2",
        "storageQuotaGiB": 11,
        "dataSizeGiB": 99,
        "collectionMetadataSchemas": "test-schema-1, test-schema-2",
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
