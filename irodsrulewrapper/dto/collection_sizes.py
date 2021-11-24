from .collection_size import CollectionSize
from typing import List, Dict, Set


class CollectionSizes:
    def __init__(self, collection_sizes: Dict[str, List[CollectionSize]], resources_set: Set):
        self.collection_sizes: Dict[str, List[CollectionSize]] = collection_sizes
        self.resources_set: Set = resources_set

    @classmethod
    def create_from_rule_result(cls, result: Dict) -> "CollectionSizes":
        collection_sizes: Dict[str, List[CollectionSize]] = {}
        resources_set = set()
        for collection_id, size_per_resource in result.items():
            collection_size_list = []
            for item in size_per_resource:
                collection_size = CollectionSize.create_from_rule_result(item)
                collection_size_list.append(collection_size)
                resources_set.add(item["resourceName"])
            collection_sizes[collection_id] = collection_size_list
        output = cls(collection_sizes, resources_set)

        return output
