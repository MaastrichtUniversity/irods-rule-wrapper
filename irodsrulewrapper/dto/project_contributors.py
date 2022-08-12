"""This module contains the ProjectContributors DTO class and its factory constructor."""
from irodsrulewrapper.dto.dto_base_model import DTOBaseModel


class ProjectContributors(DTOBaseModel):
    """This class represents the ACL role contributors for an iRODS project (=write access)."""

    contributors_users: list[str]
    contributors_groups: list[str]

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "ProjectContributors":
        contributors = cls(contributors_users=result["users"], contributors_groups=result["groups"])

        return contributors
