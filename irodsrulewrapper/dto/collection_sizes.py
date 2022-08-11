"""This module contains the CollectionSizes DTO class and its factory constructor."""
from irodsrulewrapper.dto.collection_size import CollectionSize
from irodsrulewrapper.dto.dto_base_model import DTOBaseModel


class CollectionSizes(DTOBaseModel):
    """This class represents a list of iRODS CollectionSize DTOs."""

    collection_sizes: dict[str, list[CollectionSize]]
    resources_set: set

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "CollectionSizes":
        collection_sizes: dict[str, list[CollectionSize]] = {}
        resources_set = set()
        for collection_id, size_per_resource in result.items():
            collection_size_list = []
            for item in size_per_resource:
                collection_size = CollectionSize.create_from_rule_result(item)
                collection_size_list.append(collection_size)
                resources_set.add(item["resourceName"])
            collection_sizes[collection_id] = collection_size_list
        output = cls(collection_sizes=collection_sizes, resources_set=resources_set)

        return output
