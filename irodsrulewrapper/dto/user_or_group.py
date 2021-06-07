from typing import Dict


class UserOrGroup:
    def __init__(self, user: Dict):
        self.result: Dict = user

    @classmethod
    def create_from_rule_result(cls, result: Dict) -> 'UserOrGroup':
        if result is None:
            return None
        output = cls(result)
        return output
