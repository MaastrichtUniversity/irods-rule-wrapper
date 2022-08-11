"""This module contains the CollectionDetails DTO class and its factory constructor."""
import json

from dhpythonirodsutils import formatters
from dhpythonirodsutils.enums import ProjectAVUs

from irodsrulewrapper.dto.dto_base_model import DTOBaseModel
from irodsrulewrapper.dto.external_pid import ExternalPID


class CollectionDetails(DTOBaseModel):
    """This class represents an iRODS project collection with its extended attributes."""

    id: str
    creator: str
    size: float
    title: str
    pid: str
    num_files: str
    enable_archive: bool
    enable_unarchive: bool
    enable_open_access_export: bool
    external_pid_list: list[ExternalPID]

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "CollectionDetails":
        external_pid_list = []
        if result["externals"] != "no-externalPID-set":
            for external in result["externals"]:
                external_pid_list.append(ExternalPID.create_from_rule_result(external))

        enable_archive = None
        if ProjectAVUs.ENABLE_ARCHIVE.value in result and formatters.format_string_to_boolean(
            result[ProjectAVUs.ENABLE_ARCHIVE.value]
        ):
            enable_archive = True
        elif ProjectAVUs.ENABLE_ARCHIVE.value in result and not formatters.format_string_to_boolean(
            result[ProjectAVUs.ENABLE_ARCHIVE.value]
        ):
            enable_archive = False

        enable_unarchive = None
        if ProjectAVUs.ENABLE_UNARCHIVE.value in result and formatters.format_string_to_boolean(
            result[ProjectAVUs.ENABLE_UNARCHIVE.value]
        ):
            enable_unarchive = True
        elif ProjectAVUs.ENABLE_UNARCHIVE.value in result and not formatters.format_string_to_boolean(
            result[ProjectAVUs.ENABLE_UNARCHIVE.value]
        ):
            enable_unarchive = False

        enable_open_access_export = None
        if ProjectAVUs.ENABLE_OPEN_ACCESS_EXPORT.value in result and formatters.format_string_to_boolean(
            result[ProjectAVUs.ENABLE_OPEN_ACCESS_EXPORT.value]
        ):
            enable_open_access_export = True
        elif ProjectAVUs.ENABLE_OPEN_ACCESS_EXPORT.value in result and not formatters.format_string_to_boolean(
            result[ProjectAVUs.ENABLE_OPEN_ACCESS_EXPORT.value]
        ):
            enable_open_access_export = False

        collection = cls(
            id=result["collection"],
            creator=result["creator"],
            size=result["byteSize"],
            title=result["title"],
            pid=result["PID"],
            num_files=result["numFiles"],
            enable_archive=enable_archive,
            enable_unarchive=enable_unarchive,
            enable_open_access_export=enable_open_access_export,
            external_pid_list=external_pid_list,
        )
        return collection

    @classmethod
    def create_from_mock_result(cls, mock_json=None) -> "CollectionDetails":
        if mock_json is None:
            mock_json = COLLECTION_DETAILS
        return CollectionDetails.create_from_rule_result(json.loads(mock_json))


COLLECTION_DETAILS = """
{
    "PID": "21.T12996/P000000014C000000001",
    "byteSize": 554400,
    "collection": "C000000001",
    "contributors": {
        "groupObjects": [
            {
                "description": "It's DataHub! The place to store your data.",
                "displayName": "DataHub",
                "groupId": "10122",
                "groupName": "datahub"
            }
        ],
        "groups": [
            "datahub"
        ],
        "userObjects": [
            {
                "displayName": "service-pid",
                "userId": "10107",
                "userName": "service-pid"
            }
        ],
        "users": [
            "service-pid"
        ]
    },
    "creator": "jonathan.melius@maastrichtuniversity.nl",
    "enableArchive": "true",
    "enableOpenAccessExport": "true",
    "enableUnarchive": "true",
    "exporterState": "no-state-set",
    "externals": "no-externalPID-set",
    "managers": {
        "groupObjects": [],
        "groups": [],
        "userObjects": [
            {
                "displayName": "Pascal Suppers",
                "userId": "10058",
                "userName": "psuppers"
            },
            {
                "displayName": "Olav Palmen",
                "userId": "10083",
                "userName": "opalmen"
            }
        ],
        "users": [
            "psuppers",
            "opalmen"
        ]
    },
    "numFiles": "4",
    "project": "P000000014",
    "title": "Dataset Title1",
    "viewers": {
        "groupObjects": [],
        "groups": [],
        "userObjects": [
            {
                "displayName": "service-disqover",
                "userId": "10110",
                "userName": "service-disqover"
            }
        ],
        "users": [
            "service-disqover"
        ]
    }
}
"""
