"""This module contains the CollectionFolderTree DTO class and its factory constructor."""
from irodsrulewrapper.dto.collection_tree_node import CollectionTreeNode
from irodsrulewrapper.dto.dto_base_model import DTOBaseModel


class CollectionTreeRoot(DTOBaseModel):
    """CollectionFolderTree CollectionFileTree"""

    nodes: list[CollectionTreeNode]

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "CollectionTreeRoot":
        output = []
        for item in result:
            ret = CollectionTreeNode.create_from_rule_result(item)
            output.append(ret)
        folder_tree = cls(nodes=output)
        return folder_tree
