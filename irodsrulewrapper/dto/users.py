from .user import User
from typing import List, Dict


class Users:
    def __init__(self, users: List['User']):
        self.users: List['User'] = users

    @classmethod
    def create_from_rule_result(cls, result: Dict) -> 'Users':
        output = []
        for item in result:
            user = User.create_from_rule_result(item)
            output.append(user)
        users = cls(output)
        return users
