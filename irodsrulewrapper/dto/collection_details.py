from typing import List, Dict

from dhpythonirodsutils import formatters

from irodsrulewrapper.dto.external_pid import ExternalPID


class CollectionDetails:
    def __init__(
        self,
        id: str,
        creator: str,
        size: float,
        title: str,
        pid: str,
        num_files: str,
        enable_archive: bool,
        enable_unarchive: bool,
        enable_open_access_export: bool,
        external_pid_list: List,
    ):

        self.id: str = id
        self.creator: str = creator
        self.size: float = size
        self.title: str = title
        self.pid: str = pid
        self.num_files: str = num_files
        self.enable_archive: bool = enable_archive
        self.enable_unarchive: bool = enable_unarchive
        self.enable_open_access_export: bool = enable_open_access_export
        self.external_pid_list: List = external_pid_list

    @classmethod
    def create_from_rule_result(cls, result: Dict) -> "CollectionDetails":
        external_pid_list = []
        if result["externals"] != "no-externalPID-set":
            for external in result["externals"]:
                external_pid_list.append(ExternalPID.create_from_rule_result(external))

        enable_archive = None
        if "enableArchive" in result and formatters.format_string_to_boolean(result["enableArchive"]):
            enable_archive = True
        elif "enableArchive" in result and not formatters.format_string_to_boolean(result["enableArchive"]):
            enable_archive = False

        enable_unarchive = None
        if "enableUnarchive" in result and formatters.format_string_to_boolean(result["enableUnarchive"]):
            enable_unarchive = True
        elif "enableUnarchive" in result and not formatters.format_string_to_boolean(result["enableUnarchive"]):
            enable_unarchive = False

        enable_open_access_export = None
        if "enableOpenAccessExport" in result and formatters.format_string_to_boolean(result["enableOpenAccessExport"]):
            enable_open_access_export = True
        elif "enableOpenAccessExport" in result and not formatters.format_string_to_boolean(
            result["enableOpenAccessExport"]
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
