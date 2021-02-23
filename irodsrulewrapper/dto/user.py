from typing import Dict


class User:
    def __init__(self, user_name: str, user_id: str, display_name: str):
        self.user_name: str = user_name
        self.user_id: str = user_id
        self.display_name: str = display_name

    @classmethod
    def create_from_rule_result(cls, result: Dict) -> 'User':
        user = cls(result["userName"], result["userId"], result["displayName"])
        return user
