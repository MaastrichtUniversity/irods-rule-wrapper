from typing import Dict


class MigrationCard:
    def __init__(self, collection: str, repository: str, status: str, title: str):
        self.collection: str = collection
        self.repository: str = repository
        self.status: str = status
        self.title: str = title

    @classmethod
    def create_from_rule_result(cls, result: Dict) -> "MigrationCard":
        user = cls(result["collection"], result["repository"], result["status"], result["title"])
        return user
