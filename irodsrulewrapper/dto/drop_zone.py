"""This module contains the DropZone class and its factory constructor."""
import json

from dhpythonirodsutils import formatters
from dhpythonirodsutils.enums import ProjectAVUs


class DropZone:
    """This class represents an iRODS dropzone collection with its attributes"""

    def __init__(
        self,
        date: str,
        project: str,
        project_title: str,
        state: str,
        title: str,
        token: str,
        validate_msg: str,
        validate_state: str,
        resource_status: str,
        total_size: str,
        destination: str,
        dropzone_type: str,
        creator: str,
        shared_with_me: bool,
        dropzone_sharing_enabled: bool,
    ):
        self.date: str = date
        self.project: str = project
        self.project_title: str = project_title
        self.state: str = state
        self.title: str = title
        self.token: str = token
        self.validate_msg: str = validate_msg
        self.validate_state: str = validate_state
        self.resource_status: str = resource_status
        self.total_size: str = total_size
        self.destination: str = destination
        self.type: str = dropzone_type
        self.creator: str = creator
        self.shared_with_me: bool = shared_with_me
        self.dropzone_sharing_enabled: bool = dropzone_sharing_enabled

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "DropZone":
        if "resourceStatus" not in result:
            result["resourceStatus"] = ""

        user = cls(
            result["date"],
            result["project"],
            result["projectTitle"],
            result["state"],
            result["title"],
            result["token"],
            result["validateMsg"],
            result["validateState"],
            result["resourceStatus"],
            result["totalSize"],
            result["destination"],
            result["type"],
            result["creator"],
            formatters.format_string_to_boolean(result["sharedWithMe"]),
            formatters.format_string_to_boolean(result[ProjectAVUs.ENABLE_DROPZONE_SHARING.value]),
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
