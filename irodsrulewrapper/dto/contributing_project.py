from typing import List, Dict


class ContributingProject:
    def __init__(self, id: str, title: str, managers: List[str], contributors_users: List[str],
                 contributors_groups: List[str], viewers_users: List[str], viewers_groups: List[str], resource: str):
        self.id: str = id
        self.title: str = title
        self.managers: List[str] = managers
        self.contributors_users: List[str] = contributors_users
        self.contributors_groups: List[str] = contributors_groups
        self.viewers_users: List[str] = viewers_users
        self.viewers_groups: List[str] = viewers_groups
        self.resource: str = resource

    @classmethod
    def create_from_rule_result(cls, result: Dict) -> 'ContributingProject':
        managers = result["managers"]["users"]
        contributors_users = result["contributors"]["users"]
        contributors_groups = result["contributors"]["groups"]
        viewers_users = result["viewers"]["users"]
        viewers_groups = result["viewers"]["groups"]
        resource = result["resource"]
        projects = cls(result["id"], result["title"], managers, contributors_users, contributors_groups, viewers_users,
                       viewers_groups, resource)

        return projects
