"""This module contains the User DTO class and its factory constructor."""

from pydantic import BaseModel


class User(BaseModel):
    """This class represents an iRODS user with its minimal attributes"""

    user_name: str
    user_id: str
    display_name: str

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "User":
        user = cls(user_name=result["userName"], user_id=result["userId"], display_name=result["displayName"])
        return user
