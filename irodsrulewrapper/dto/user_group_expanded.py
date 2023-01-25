"""This module contains the UserGroupExpanded DTO class and its factory constructor."""
from pydantic import BaseModel


class UserGroupExpanded(BaseModel):
    """This class represents a minimal UserGroupExtended object."""

    display_name: str
    email: str

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "UserGroupExpanded":
        project = cls(
            display_name=result["displayName"],
            email=result["email"] if "email" in result else "",
        )
        return project
