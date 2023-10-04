"""This module contains the Collection DTO class and its factory constructor."""
from dhpythonirodsutils import formatters
from dhpythonirodsutils.enums import ProjectAVUs


class Collection:
    """This class represents an iRODS project collection with its attributes."""

    def __init__(
        self,
        collection_id: str,
        creator: str,
        size: float,
        title: str,
        pid: str,
        num_files: int,
        num_user_files: int,
        enable_archive: bool,
        enable_unarchive: bool,
    ):

        self.id: str = collection_id
        self.creator: str = creator
        self.size: float = size
        self.title: str = title
        self.pid: str = pid
        self.num_files: int = num_files
        self.num_user_files: int = num_user_files
        self.enable_archive: bool = enable_archive
        self.enable_unarchive: bool = enable_unarchive

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

        collection = cls(
            collection_id,
            result["creator"],
            size,
            result["title"],
            result["PID"],
            result["numFiles"],
            result["numUserFiles"],
            enable_archive,
            enable_unarchive,
        )
        return collection
