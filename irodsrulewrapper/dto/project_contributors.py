"""This module contains the ProjectContributors DTO class and its factory constructor."""


class ProjectContributors:
    """This class represents the ACL role contributors for an iRODS project (=write access)."""

    def __init__(
        self,
        contributors_users: list,
        contributors_groups: list,
    ):
        self.contributors_users: list = contributors_users
        self.contributors_groups: list = contributors_groups

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "ProjectContributors":
        contributors = cls(result["users"], result["groups"])

        return contributors
