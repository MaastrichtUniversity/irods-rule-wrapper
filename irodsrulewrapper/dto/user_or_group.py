"""This module contains the UserOrGroup DTO class and its factory constructor."""


class UserOrGroup:
    """
    This class is part of the Browser Cache Time To Live (TTL) flow.
    It represents the rule output of UserRuleManager.get_user_or_group_by_id().
    It can be used to either create a User DTO or a Group DTO in UserRuleManager.get_user_or_group().
    The DTO is then stored in the dictionary CacheTTL.CACHE_USERS_GROUPS.
    """

    def __init__(self, result: dict):
        self.result: dict = result

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "UserOrGroup":
        if result is None:
            return None
        output = cls(result)
        return output
