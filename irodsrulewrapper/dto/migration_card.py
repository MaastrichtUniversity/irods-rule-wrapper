"""This module contains the MigrationCard DTO class and its factory constructor."""
from irodsrulewrapper.dto.dto_base_model import DTOBaseModel


class MigrationCard(DTOBaseModel):
    """This class represents an ongoing project collection migration with its attributes."""

    collection: str
    repository: str
    status: str
    title: str

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "MigrationCard":
        user = cls(
            collection=result["collection"],
            repository=result["repository"],
            status=result["status"],
            title=result["title"],
        )
        return user
