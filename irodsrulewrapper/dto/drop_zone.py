"""This module contains the DropZone class and its factory constructor."""
import json

from dhpythonirodsutils import formatters
from dhpythonirodsutils.enums import ProjectAVUs

from irodsrulewrapper.dto.dto_base_model import DTOBaseModel


class DropZone(DTOBaseModel):
    """This class represents an iRODS dropzone collection with its attributes"""

    date: str
    project: str
    project_title: str
    state: str
    title: str
    token: str
    validate_msg: str
    validate_state: str
    resource_status: str
    total_size: str
    destination: str
    type: str
    creator: str
    shared_with_me: bool
    dropzone_sharing_enabled: bool
    progress: float = 0.0

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "DropZone":
        if "resourceStatus" not in result:
            result["resourceStatus"] = ""

        user = cls(
            date=result["date"],
            project=result["project"],
            project_title=result["projectTitle"],
            state=result["state"],
            title=result["title"],
            token=result["token"],
            validate_msg=result["validateMsg"],
            validate_state=result["validateState"],
            resource_status=result["resourceStatus"],
            total_size=result["totalSize"],
            destination=result["destination"],
            type=result["type"],
            creator=result["creator"],
            shared_with_me=formatters.format_string_to_boolean(result["sharedWithMe"]),
            dropzone_sharing_enabled=formatters.format_string_to_boolean(
                result[ProjectAVUs.ENABLE_DROPZONE_SHARING.value]
            ),
        )
        return user

    @classmethod
    def create_from_mock_result(cls, mock_json=None) -> "DropZone":
        if mock_json is None:
            mock_json = DROPZONE
        return DropZone.create_from_rule_result(json.loads(mock_json))


DROPZONE = """
  {
    "totalSize": "521844260",
    "token": "prickly-caracal",
    "type": "mounted",
    "sharedWithMe": "true",
    "state": "error-post-ingestion",
    "validateMsg": "N/A",
    "project": "P000000014",
    "title": "Test sprint 1",
    "validateState": "N/A",
    "projectTitle": "Hope that the day after you die is a nice day.",
    "enableDropzoneSharing": "true",
    "date": "01659701010",
    "creator": "jmelius",
    "destination": "C000000001",
    "startDate": "2022-08-05",
    "userName": "N/A",
    "endDate": "2022-11-03"
  }
"""
