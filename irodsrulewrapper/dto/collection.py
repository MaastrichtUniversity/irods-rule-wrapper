from dhpythonirodsutils import formatters
from dhpythonirodsutils.enums import ProjectAVUs


class Collection:
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
        enable_open_access_export: bool,
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
        self.enable_open_access_export: bool = enable_open_access_export

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
            collection_id,
            result["creator"],
            size,
            result["title"],
            result["PID"],
            result["numFiles"],
            result["numUserFiles"],
            enable_archive,
            enable_unarchive,
            enable_open_access_export,
        )
        return collection
