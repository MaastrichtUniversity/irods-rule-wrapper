from typing import Dict


class Boolean:
    def __init__(self, boolean: bool):
        self.boolean: str = boolean

    @classmethod
    def create_from_rule_result(cls, result: Dict) -> "Boolean":
        boolean = cls(result)
        return boolean
