"""This module contains the DataSteward class and its factory constructor."""


class DataSteward:
    """
    This class represents an iRODS data steward user with its minimal attributes.

    TO_REFACTOR: Replace DataSteward usage by User DTO
    """

    def __init__(self, user_name: str, user_id: str, display_name: str):
        self.user_name: str = user_name
        self.user_id: str = user_id
        self.display_name: str = display_name

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "DataSteward":
        data_steward = cls(result["userName"], result["userId"], result["displayName"])
        return data_steward
