from .collection_size import CollectionSize
from typing import List, Dict


class CollectionSizes:
    def __init__(self, collection_sizes: List['CollectionSize']):
        self.collection_sizes: List['CollectionSize'] = collection_sizes

    @classmethod
    def create_from_rule_result(cls, result: Dict) -> 'CollectionSizes':
        output = []
        for item in result:
            collection_size = CollectionSize.create_from_rule_result(item)
            output.append(collection_size)
        collection_sizes = cls(output)
        return collection_sizes