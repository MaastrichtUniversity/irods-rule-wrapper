"""This module contains the Collection DTO class and its factory constructor."""
from dhpythonirodsutils import formatters
from dhpythonirodsutils.enums import ProjectAVUs

from irodsrulewrapper.dto.dto_base_model import DTOBaseModel


class Collection(DTOBaseModel):
    """This class represents an iRODS project collection with its attributes."""

    id: str
    creator: str
    size: float
    title: str
    pid: str
    num_files: int
    num_user_files: int
    enable_archive: bool
    enable_unarchive: bool
    enable_open_access_export: bool

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "Collection":
        collection_id = ""
        if "id" in result:
            collection_id = result["id"]
        elif "collection" in result:
            collection_id = result["collection"]

        size = ""
        if "size" in result:
            size = result["size"]
        elif "byteSize" in result:
            size = result["byteSize"]

        enable_archive = False
        if ProjectAVUs.ENABLE_ARCHIVE.value in result and formatters.format_string_to_boolean(
            result[ProjectAVUs.ENABLE_ARCHIVE.value]
        ):
            enable_archive = True
        elif ProjectAVUs.ENABLE_ARCHIVE.value in result and not formatters.format_string_to_boolean(
            result[ProjectAVUs.ENABLE_ARCHIVE.value]
        ):
            enable_archive = False

        enable_unarchive = False
        if ProjectAVUs.ENABLE_UNARCHIVE.value in result and formatters.format_string_to_boolean(
            result[ProjectAVUs.ENABLE_UNARCHIVE.value]
        ):
            enable_unarchive = True
        elif ProjectAVUs.ENABLE_UNARCHIVE.value in result and not formatters.format_string_to_boolean(
            result[ProjectAVUs.ENABLE_UNARCHIVE.value]
        ):
            enable_unarchive = False

        enable_open_access_export = False
        if ProjectAVUs.ENABLE_OPEN_ACCESS_EXPORT.value in result and formatters.format_string_to_boolean(
            result[ProjectAVUs.ENABLE_OPEN_ACCESS_EXPORT.value]
        ):
            enable_open_access_export = True
        elif ProjectAVUs.ENABLE_OPEN_ACCESS_EXPORT.value in result and not formatters.format_string_to_boolean(
            result[ProjectAVUs.ENABLE_OPEN_ACCESS_EXPORT.value]
        ):
            enable_open_access_export = False

        collection = cls(
            id=collection_id,
            creator=result["creator"],
            size=size,
            title=result["title"],
            pid=result["PID"],
            num_files=result["numFiles"],
            num_user_files=result["numUserFiles"],
            enable_archive=enable_archive,
            enable_unarchive=enable_unarchive,
            enable_open_access_export=enable_open_access_export,
        )
        return collection
