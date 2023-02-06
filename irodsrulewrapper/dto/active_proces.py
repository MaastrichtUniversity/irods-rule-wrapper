"""This module contains the ActiveProcess DTO class and its factory constructor."""


class ActiveProcess:
    """This class represents an ongoing project collection active process with its attributes."""

    def __init__(self, collection: str, repository: str, status: str, title: str, project: str, project_title: str):
        self.collection: str = collection
        self.repository: str = repository
        self.status: str = status
        self.title: str = title
        self.project: str = project
        self.project_title: str = project_title

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "ActiveProcess":
        card = cls(
            result["collection"],
            result["repository"],
            result["state"],
            result["title"],
            result["project"],
            result["project_title"],
        )
        return card
