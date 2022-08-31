"""This module contains the ProjectMinimal DTO class and its factory constructor."""
from pydantic import BaseModel


class ProjectMinimal(BaseModel):
    """This class represents an iRODS project with its minimal attributes."""

    id: str
    title: str

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "ProjectMinimal":
        project = cls(
            id=result["id"],
            title=result["title"],
        )
        return project
