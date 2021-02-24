from typing import Dict


class Group:
    def __init__(self, name: str, group_id: str, display_name: str, description: str):
        self.name: str = name
        self.id: str = group_id
        self.display_name: str = display_name
        self.description: str = description

    @classmethod
    def create_from_rule_result(cls, result: Dict) -> 'Group':
        # Backward compatibility
        name = ''
        if "userName" in result:
            name = result["userName"]
        elif "name" in result:
            name = result["name"]
        group_id = ''
        if "userId" in result:
            group_id = result["userId"]
        elif "groupId" in result:
            group_id = result["groupId"]

        group = cls(name, group_id, result["displayName"], result["description"])
        return group
