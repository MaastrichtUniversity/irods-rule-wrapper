from .collection import Collection
from typing import List, Dict


class Collections:
    def __init__(self, collections):
        self.collections = collections

    @classmethod
    def create_from_rule_result(cls, result: Dict) -> 'Collections':
        collections = []
        for item in result:
            collection = Collection.create_from_rule_result(item)
            collections.append(collection)
        output = cls(collections)
        return output
