from irodsrulewrapper.dto.collection import Collection


class Collections:
    def __init__(self, collections: list["Collection"]):
        self.collections: list["Collection"] = collections

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "Collections":
        collections = []
        for item in result:
            collection = Collection.create_from_rule_result(item)
            collections.append(collection)
        output = cls(collections)
        return output
