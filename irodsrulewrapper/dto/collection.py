from typing import Dict


class Collection:
    def __init__(self, id: str, creator: str, size: float, title: str, pid: str, num_files: str):
        self.id: str = id
        self.creator: str = creator
        self.size: float = size
        self.title: str = title
        self.pid: str = pid
        self.num_files: str = num_files

    @classmethod
    def create_from_rule_result(cls, result: Dict) -> 'Collection':
        collection = cls(result["id"], result["creator"], result["size"],
                         result["title"], result["PID"], result["numFiles"])
        return collection
