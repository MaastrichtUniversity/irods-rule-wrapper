"""
This module contains the dataclass and functions to convert iRODS uid into a User or Group DTO.
"""
from dataclasses import dataclass

from irodsrulewrapper.cache import CacheTTL
from irodsrulewrapper.dto.group import Group
from irodsrulewrapper.dto.user import User
from irodsrulewrapper.rule_managers.users import UserRuleManager


@dataclass
class UserGroups:
    """
    Simple dataclass to store all the different level of permissions for users or groups
    """

    manager_users: list
    contributor_users: list
    contributor_groups: list
    viewer_users: list
    viewer_groups: list


def convert_uids_to_users_or_groups(result):
    """
    Takes the users ids from the rule output and convert them as User or Group DTOs.

    Parameters
    ----------
    result: dict
        The json rule output of the rule "optimized_list_projects"

    Returns
    -------
    UserGroups
        Contains the converted uid as User or Group DTO
    """
    output = UserGroups(
        manager_users=[], contributor_users=[], contributor_groups=[], viewer_users=[], viewer_groups=[]
    )
    rule_manager = UserRuleManager("service-disqover")
    for manager_uid in result["managers"]:
        manager = get_user_or_group(manager_uid, rule_manager)
        if isinstance(manager, User):
            output.manager_users.append(manager)

    for contributor_uid in result["contributors"]:
        contributor = get_user_or_group(contributor_uid, rule_manager)
        if isinstance(contributor, User):
            output.contributor_users.append(contributor)
        elif isinstance(contributor, Group):
            output.contributor_groups.append(contributor)

    for viewer_uid in result["viewers"]:
        viewer = get_user_or_group(viewer_uid, rule_manager)
        if isinstance(viewer, User):
            output.viewer_users.append(viewer)
        elif isinstance(viewer, Group):
            output.viewer_groups.append(viewer)

    rule_manager.session.cleanup()

    return output


def get_user_or_group(uid: str, rule_manager):
    """
    Retrieve a user or group DTO based on the input uid.
    First check if the uid is present the cached dict. Otherwise, query the uid.

    Parameters
    ----------
    uid: str
        The uid to query and retrieve from the cache
    rule_manager: RuleManager

    Returns
    -------
    User|Group
        The DTO of the input uid
    """
    if uid not in CacheTTL.CACHE_USERS_GROUPS:
        # rodsadmin and service-account UIDs are filtered in the rule
        item = rule_manager.get_user_or_group_by_id(uid)
        if item.result["account_type"] == "rodsuser":
            CacheTTL.CACHE_USERS_GROUPS[uid] = User.create_from_rule_result(item.result)
        elif item.result["account_type"] == "rodsgroup":
            CacheTTL.CACHE_USERS_GROUPS[uid] = Group.create_from_rule_result(item.result)

    return CacheTTL.CACHE_USERS_GROUPS[uid]
