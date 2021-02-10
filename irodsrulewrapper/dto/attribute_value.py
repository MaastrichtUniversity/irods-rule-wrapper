class AttributeValue:
    def __init__(self, value):
        self.value = value

    @classmethod
    def create_from_rule_result(cls, result):
        value = cls(result["value"])
        return value
