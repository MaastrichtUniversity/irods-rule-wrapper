"""This module contains the Group DTO class and its factory constructor."""
from pydantic import BaseModel


class Group(BaseModel):
    """This class represents an iRODS group with its attributes"""

    name: str
    id: str
    display_name: str
    description: str
    # def __init__(self, name: str, group_id: str, display_name: str, description: str):
    #     self.name: str = name
    #     self.id: str = group_id
    #     self.display_name: str = display_name
    #     self.description: str = description

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "Group":
        # Backward compatibility
        name = ""
        if "userName" in result:
            name = result["userName"]
        elif "name" in result:
            name = result["name"]
        group_id = ""
        if "userId" in result:
            group_id = result["userId"]
        elif "groupId" in result:
            group_id = result["groupId"]

        group = cls(name=name, id=group_id, display_name=result["displayName"], description=result["description"])
        return group
