"""This module contains the CollectionItemTree DTO class and its factory constructor."""
from irodsrulewrapper.dto.dto_base_model import DTOBaseModel


class CollectionItemTree(DTOBaseModel):
    """CollectionFolderTree CollectionFileTree"""

    ctime: str
    mtime: str
    name: str
    offlineResource: bool
    path: str
    rescname: str
    size: str
    type: str

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "CollectionItemTree":
        item = cls(
            ctime=result["ctime"],
            mtime=result["mtime"],
            name=result["name"],
            offlineResource=result["offlineResource"],
            path=result["path"],
            rescname=result["rescname"],
            size=result["size"],
            type=result["type"],
        )
        return item
