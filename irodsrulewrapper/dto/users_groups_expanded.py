"""This module contains the UsersGroupsExpanded DTO class, its factory constructors and mock_json."""
import json

from pydantic import BaseModel
from typing import Dict

from irodsrulewrapper.dto.user_group_expanded import UserGroupExpanded


class UsersGroupsExpanded(BaseModel):
    """
    This class represents a dictionary of iRODS UsersGroupsExpanded DTOs.
    The expanded part means all the members of a group have been queried and added to the dictionary attribute
    user_groups.
    It overwrites __iter__, __getitem__ & __len__ methods to make the UsersGroupsExpanded object behave like a
    dictionary.
    """

    user_groups: Dict[str, UserGroupExpanded]

    def __iter__(self):
        return iter(self.user_groups)

    def __getitem__(self, item):
        return self.user_groups[item]

    def __len__(self):
        return len(self.user_groups)

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "UsersGroupsExpanded":
        expanded_users_groups_list = {}
        for name, attribute in result.items():
            user_group = UserGroupExpanded.create_from_rule_result(attribute)
            expanded_users_groups_list[name] = user_group
        output = cls(user_groups=expanded_users_groups_list)
        return output

    @classmethod
    def create_from_mock_result(cls, projects_json=None) -> "UsersGroupsExpanded":
        if projects_json is None:
            projects_json = USERS_GROUPS_JSON
        return UsersGroupsExpanded.create_from_rule_result(json.loads(projects_json))


USERS_GROUPS_JSON: str = """
{
    "auser": {
        "displayName": "Additional User newly created in LDAP",
        "email": "auser"
    },
    "datahub": {
        "displayName": "DataHub"
    },
    "dlinssen": {
        "displayName": "Dean Linssen",
        "email": "dlinssen@um.nl"
    },
    "dtheuniss": {
        "displayName": "Dani\u00ebl Theunissen",
        "email": "dtheunissen@um.nl"
    },
    "jmelius": {
        "displayName": "Jonathan M\u00e9lius",
        "email": "jmelius@um.nl"
    },
    "opalmen": {
        "displayName": "Olav Palmen",
        "email": "opalmen@um.nl"
    },
    "psuppers": {
        "displayName": "Pascal Suppers",
        "email": "psuppers@um.nl"
    },
    "pvanschay2": {
        "displayName": "Paul van Schayck",
        "email": "pvanschayck@um.nl"
    },
    "rvoncken": {
        "displayName": "Rickest Rick",
        "email": "rvoncken@example.org"
    },
    "scannexus": {
        "displayName": "SCANNEXUS"
    }
}
"""
