"""This module contains the ProjectsOverview DTO class and its factory constructor."""
import json

from irodsrulewrapper.dto.dto_base_model import DTOBaseModel
from irodsrulewrapper.cache import CacheTTL
from irodsrulewrapper.dto.project_overview import ProjectOverview


class ProjectsOverview(DTOBaseModel):
    """
    This class represents a list of iRODS ProjectsOverview DTOs.
    """

    projects: list[ProjectOverview]

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "ProjectsOverview":
        CacheTTL.check_if_cache_expired()
        output = []
        for item in result:
            project = ProjectOverview.create_from_rule_result(
                item,
            )
            output.append(project)
        projects = cls(projects=output)
        return projects

    @classmethod
    def create_from_mock_result(cls, projects_json=None) -> "ProjectsOverview":
        if projects_json is None:
            projects_json = PROJECTS_OVERVIEW
        return ProjectsOverview.create_from_rule_result(json.loads(projects_json))


PROJECTS_OVERVIEW = """
[
    {
        "OBI:0000103": "pvanschay2",
        "archiveDestinationResource": "arcRescSURF01",
        "authorizationPeriodEndDate": "1-1-2018",
        "collectionMetadataSchemas": "DataHub_general_schema,DataHub_extended_schema",
        "contributors": [
            "10126"
        ],
        "dataRetentionPeriodEndDate": "1-1-2018",
        "dataSizeGiB": 0.0,
        "dataSteward": "pvanschay2",
        "enableArchive": "true",
        "enableContributorEditMetadata": "false",
        "enableDropzoneSharing": "true",
        "enableOpenAccessExport": "false",
        "enableUnarchive": "true",
        "ingestResource": "iresResource",
        "managers": [
            "10055"
        ],
        "path": "P000000012",
        "resource": "replRescUM01",
        "responsibleCostCenter": "UM-12345678901B",
        "storageQuotaGb": "10",
        "title": "You recoil from the crude; you tend naturally toward the exquisite.",
        "viewers": []
    },
    {
        "OBI:0000103": "pvanschay2",
        "archiveDestinationResource": "arcRescSURF01",
        "authorizationPeriodEndDate": "1-1-2018",
        "collectionMetadataSchemas": "DataHub_general_schema,DataHub_extended_schema",
        "contributors": [
            "10126"
        ],
        "dataRetentionPeriodEndDate": "1-1-2018",
        "dataSizeGiB": 0.0,
        "dataSteward": "pvanschay2",
        "enableArchive": "true",
        "enableContributorEditMetadata": "false",
        "enableDropzoneSharing": "true",
        "enableOpenAccessExport": "false",
        "enableUnarchive": "true",
        "ingestResource": "iresResource",
        "managers": [
            "10055"
        ],
        "path": "P000000013",
        "resource": "replRescUM01",
        "responsibleCostCenter": "UM-12345678901B",
        "storageQuotaGb": "10",
        "title": "You will soon forget this.",
        "viewers": []
    },
    {
        "OBI:0000103": "psuppers",
        "archiveDestinationResource": "arcRescSURF01",
        "archiveState": "archive-done",
        "authorizationPeriodEndDate": "1-1-2018",
        "collectionMetadataSchemas": "DataHub_general_schema,DataHub_extended_schema",
        "contributors": [
            "10129"
        ],
        "dataRetentionPeriodEndDate": "1-1-2018",
        "dataSizeGiB": 0.9723356142640114,
        "dataSteward": "opalmen",
        "enableArchive": "true",
        "enableContributorEditMetadata": "false",
        "enableDropzoneSharing": "true",
        "enableOpenAccessExport": "true",
        "enableUnarchive": "true",
        "exporterState": "DataverseNL:in-queue-for-export",
        "ingestResource": "iresResource",
        "managers": [
            "10060",
            "10085"
        ],
        "path": "P000000014",
        "resource": "replRescUM01",
        "responsibleCostCenter": "UM-01234567890X",
        "storageQuotaGb": "10",
        "title": "Hope that the day after you die is a nice day.",
        "viewers": []
    },
    {
        "OBI:0000103": "psuppers",
        "archiveDestinationResource": "arcRescSURF01",
        "authorizationPeriodEndDate": "1-1-2018",
        "collectionMetadataSchemas": "DataHub_general_schema,DataHub_extended_schema",
        "contributors": [
            "10129"
        ],
        "dataRetentionPeriodEndDate": "1-1-2018",
        "dataSizeGiB": 0.0,
        "dataSteward": "opalmen",
        "enableArchive": "true",
        "enableContributorEditMetadata": "false",
        "enableDropzoneSharing": "true",
        "enableOpenAccessExport": "true",
        "enableUnarchive": "true",
        "ingestResource": "iresResource",
        "managers": [
            "10060",
            "10085"
        ],
        "path": "P000000015",
        "resource": "replRescUM01",
        "responsibleCostCenter": "UM-01234567890X",
        "storageQuotaGb": "10",
        "title": "Your society will be sought by people of taste and refinement.",
        "viewers": []
    }
]
"""
