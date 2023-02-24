"""This module contains the ActiveProcess DTO class and its factory constructor."""
from pydantic import BaseModel


class ActiveProcess(BaseModel):
    """This class represents an ongoing project collection active process with its attributes."""

    repository: str
    status: str
    collection_id: str
    collection_title: str
    project_id: str
    project_title: str
    process_id: str
    process_type: str

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "ActiveProcess":
        card = cls(
            repository=result["repository"],
            status=result["state"],
            collection_id=result["collection_id"],
            collection_title=result["collection_title"],
            project_id=result["project_id"],
            project_title=result["project_title"],
            process_id=result["process_id"],
            process_type=result["process_type"],
        )

        return card
