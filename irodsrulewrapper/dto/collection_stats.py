"""This module contains the CollectionStats DTO class and its factory constructor."""
from pydantic import BaseModel


class CollectionStats(BaseModel):
    """
    This class represents some statistics for an iRODS collection.
    "total_file_count" : int: The total number of files in the collection
    "total_file_size" : int : The total collection size in bytes
    """

    total_file_count: int
    total_file_size: int

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "CollectionStats":
        stats = cls(
            total_file_count=result["total_file_count"],
            total_file_size=result["total_file_size"],
        )
        return stats
