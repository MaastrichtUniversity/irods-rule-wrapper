from typing import List, Dict


class ProjectContributors:
    def __init__(
        self,
        contributors_users: List,
        contributors_groups: List,
    ):
        self.contributors_users: List = contributors_users
        self.contributors_groups: List = contributors_groups

    @classmethod
    def create_from_rule_result(cls, result: Dict) -> "ProjectContributors":
        contributors = cls(result["users"], result["groups"])

        return contributors
