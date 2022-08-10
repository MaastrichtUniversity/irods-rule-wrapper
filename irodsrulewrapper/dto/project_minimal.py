"""This module contains the ProjectMinimal DTO class and its factory constructor."""
from irodsrulewrapper.dto.dto_base_model import DTOBaseModel


class ProjectMinimal(DTOBaseModel):
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
