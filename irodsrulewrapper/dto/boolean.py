class Boolean:
    def __init__(self, boolean: bool):
        self.boolean: bool = boolean

    @classmethod
    def create_from_rule_result(cls, result: bool) -> "Boolean":
        boolean = cls(result)
        return boolean
