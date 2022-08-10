"""This module contains the CollectionFolderTree DTO class and its factory constructor."""

from irodsrulewrapper.dto.CollectionItemTree import CollectionItemTree
from irodsrulewrapper.dto.dto_base_model import DTOBaseModel


class CollectionFolderTree(DTOBaseModel):
    """CollectionFolderTree CollectionFileTree"""

    items: list[CollectionItemTree]

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "CollectionFolderTree":
        output = []
        for item in result:
            ret = CollectionItemTree.create_from_rule_result(item)
            output.append(ret)
        folder_tree = cls(items=output)
        return folder_tree
