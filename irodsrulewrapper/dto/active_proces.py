"""This module contains the ActiveProcess DTO class and its factory constructor."""


class ActiveProcess:
    """This class represents an ongoing project collection active process with its attributes."""

    def __init__(
        self,
        collection_id: str,
        repository: str,
        status: str,
        collection_title: str,
        project_id: str,
        project_title: str,
        process_id: str,
        process_type: str,
    ):
        self.collection_id: str = collection_id
        self.repository: str = repository
        self.status: str = status
        self.collection_title: str = collection_title
        self.project_id: str = project_id
        self.project_title: str = project_title
        self.process_id: str = process_id
        self.process_type: str = process_type

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "ActiveProcess":
        card = cls(
            result["collection_id"],
            result["repository"],
            result["state"],
            result["collection_title"],
            result["project_id"],
            result["project_title"],
            result["process_id"],
            result["process_type"],
        )
        return card
