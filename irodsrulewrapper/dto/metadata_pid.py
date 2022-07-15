class MetadataPID:
    def __init__(self, instance: dict, collection: dict, schema: dict):
        self.instance: dict = instance
        self.collection: dict = collection
        self.schema: dict = schema

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "MetadataPID":
        value = cls(result["instance"], result["collection"], result["schema"])
        return value
