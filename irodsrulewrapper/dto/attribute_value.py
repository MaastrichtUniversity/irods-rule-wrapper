from typing import Dict


class AttributeValue:
    def __init__(self, value: str):
        self.value: str = value

    @classmethod
    def create_from_rule_result(cls, result: Dict) -> 'AttributeValue':
        value = cls(result["value"])
        return value
