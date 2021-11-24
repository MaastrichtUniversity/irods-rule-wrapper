from typing import Dict


class Token:
    def __init__(self, token: str):
        self.token: str = token

    @classmethod
    def create_from_rule_result(cls, result: Dict) -> "Token":
        token = cls(result)
        return token
