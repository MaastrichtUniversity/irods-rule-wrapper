from typing import Dict


class Collection:
    def __init__(
        self,
        id: str,
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

        self.id: str = id
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
    def create_from_rule_result(cls, result: Dict) -> "Collection":
        id = ""
        if "id" in result:
            id = result["id"]
        elif "collection" in result:
            id = result["collection"]

        size = ""
        if "size" in result:
            size = result["size"]
        elif "byteSize" in result:
            size = result["byteSize"]

        enable_archive = None
        if "enableArchive" in result and result["enableArchive"] == "true":
            enable_archive = True
        elif "enableArchive" in result and result["enableArchive"] == "false":
            enable_archive = False

        enable_unarchive = None
        if "enableUnarchive" in result and result["enableUnarchive"] == "true":
            enable_unarchive = True
        elif "enableUnarchive" in result and result["enableUnarchive"] == "false":
            enable_unarchive = False

        enable_open_access_export = None
        if "enableOpenAccessExport" in result and result["enableOpenAccessExport"] == "true":
            enable_open_access_export = True
        elif "enableOpenAccessExport" in result and result["enableOpenAccessExport"] == "false":
            enable_open_access_export = False

        collection = cls(
            id,
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
