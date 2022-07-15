from dhpythonirodsutils import formatters
from dhpythonirodsutils.enums import ProjectAVUs

from irodsrulewrapper.dto.external_pid import ExternalPID


class CollectionDetails:
    def __init__(
        self,
        collection_id: str,
        creator: str,
        size: float,
        title: str,
        pid: str,
        num_files: str,
        enable_archive: bool,
        enable_unarchive: bool,
        enable_open_access_export: bool,
        external_pid_list: list,
    ):

        self.id: str = collection_id
        self.creator: str = creator
        self.size: float = size
        self.title: str = title
        self.pid: str = pid
        self.num_files: str = num_files
        self.enable_archive: bool = enable_archive
        self.enable_unarchive: bool = enable_unarchive
        self.enable_open_access_export: bool = enable_open_access_export
        self.external_pid_list: list = external_pid_list

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
            result["collection"],
            result["creator"],
            result["byteSize"],
            result["title"],
            result["PID"],
            result["numFiles"],
            enable_archive,
            enable_unarchive,
            enable_open_access_export,
            external_pid_list,
        )
        return collection
