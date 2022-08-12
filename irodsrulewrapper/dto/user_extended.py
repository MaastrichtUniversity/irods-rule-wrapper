"""This module contains the UserExtended DTO class, its factory constructors and mock_json."""
import json

from irodsrulewrapper.dto.dto_base_model import DTOBaseModel


class UserExtended(DTOBaseModel):
    """This class represents an iRODS user with its extended attributes."""

    username: str
    display_name: str
    given_name: str
    family_name: str
    email: str

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "UserExtended":
        user = cls(
            username=result["username"],
            display_name=result["displayName"],
            given_name=result["givenName"],
            family_name=result["familyName"],
            email=result["email"],
        )

        return user

    @classmethod
    def create_from_mock_result(cls, user_json=None) -> "UserExtended":
        if user_json is None:
            user_json = USER_METADATA

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
