from typing import Dict


class Resource:
    def __init__(self, name: str, comment: str):
        self.name: str = name
        self.comment: str = comment

    @classmethod
    def create_from_rule_result(cls, result: Dict) -> 'Resource':
        resource = cls(result["name"], result["comment"])
        return resource
