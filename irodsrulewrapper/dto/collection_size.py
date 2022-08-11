"""This module contains the CollectionSize DTO class and its factory constructor."""
from irodsrulewrapper.dto.dto_base_model import DTOBaseModel


class CollectionSize(DTOBaseModel):
    """This class represents the data size distribution for an iRODS project collection."""

    resource: str
    size: float
    relative_size: float

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "CollectionSize":
        collection_size = cls(
            resource=result["resourceName"], size=float(result["size"]), relative_size=float(result["relativeSize"])
        )

        return collection_size
