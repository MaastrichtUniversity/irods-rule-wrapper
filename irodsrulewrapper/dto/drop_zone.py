"""This module contains the DropZone class and its factory constructor."""
from dhpythonirodsutils import formatters
from dhpythonirodsutils.enums import ProjectAVUs
from pydantic import BaseModel


class DropZone(BaseModel):
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
    process_type: str
    percentage_ingested: float
    shared_with_me: bool
    dropzone_sharing_enabled: bool

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
            process_type=result["process_type"],
            percentage_ingested=float(result["percentage_ingested"]),
            shared_with_me=formatters.format_string_to_boolean(result["sharedWithMe"]),
            dropzone_sharing_enabled=formatters.format_string_to_boolean(
                result[ProjectAVUs.ENABLE_DROPZONE_SHARING.value]
            ),
        )

        return user
