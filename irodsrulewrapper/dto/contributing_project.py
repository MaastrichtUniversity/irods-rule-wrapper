from typing import List, Dict
from .users import Users
from .groups import Groups


class ContributingProject:
    def __init__(self, id: str, title: str, managers: Users, contributors_users: Users,
                 contributors_groups: Groups, viewers_users: Users, viewers_groups: Groups, resource: str):
        self.id: str = id
        self.title: str = title
        self.managers: Users = managers
        self.contributors_users: Users = contributors_users
        self.contributors_groups: Groups = contributors_groups
        self.viewers_users: Users = viewers_users
        self.viewers_groups: Groups = viewers_groups
        self.resource: str = resource

    @classmethod
    def create_from_rule_result(cls, result: Dict) -> 'ContributingProject':
        # get_contributing_project returns an empty list, if the user is not a contributor for the project
        if len(result) == 0:
            return None

        managers = Users.create_from_rule_result(result['managers']['userObjects'])
        contributors_users = Users.create_from_rule_result(result['contributors']['userObjects'])
        contributors_groups = Groups.create_from_rule_result(result['contributors']['groupObjects'])
        viewers_users = Users.create_from_rule_result(result['viewers']['userObjects'])
        viewers_groups = Groups.create_from_rule_result(result['viewers']['groupObjects'])
        resource = result["resource"]
        projects = cls(result["id"], result["title"], managers, contributors_users, contributors_groups, viewers_users,
                       viewers_groups, resource)

        return projects
