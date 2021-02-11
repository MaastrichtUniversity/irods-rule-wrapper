class Resource:
    def __init__(self, name, comment):
        self.name = name
        self.comment = comment

    @classmethod
    def create_from_rule_result(cls, result):
        resource = cls(result["name"], result["comment"])
        return resource
