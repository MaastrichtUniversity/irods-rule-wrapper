import json

from typing import Dict


class UserExtended:
    def __init__(self, username: str, display_name: str, given_name: str, family_name: str, email: str):
        self.username: str = username
        self.display_name: str = display_name
        self.given_name: str = given_name
        self.family_name: str = family_name
        self.email: str = email

    @classmethod
    def create_from_rule_result(cls, result: Dict) -> "UserExtended":
        user = cls(
            result["username"], result["displayName"], result["givenName"], result["familyName"], result["email"]
        )

        return user

    @classmethod
    def create_from_mock_result(cls, user_json=None) -> "UserExtended":
        if user_json is None:
            user_json = cls.USER_METADATA

        return UserExtended.create_from_rule_result(json.loads(user_json))

    USER_METADATA = """
    {
        "displayName": "Olav Palmen",
        "email": "o.palmen@maastrichtuniversity.nl",
        "familyName": "Palmen",
        "givenName": "Olav",
        "username": "opalmen"     
    }
    """
