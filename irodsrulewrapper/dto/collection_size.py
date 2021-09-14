from typing import List, Dict


class CollectionSize:
    def __init__(self, collection: str, resource: str, resource_attr: str, size: str, relative_size: str):
        self.collection: str = collection
        self.resource: str = resource
        self.resource_attr: str = resource_attr
        self.size: str = size
        self.relative_size: str = relative_size

    @classmethod
    def create_from_rule_result(cls, result: Dict) -> 'CollectionSize':
        collection_size = cls(result["collection"], result["resource"], result["resourceAttr"], result["size"], result["relative_size"])
        return collection_size