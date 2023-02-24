"""This module contains the DropZones class and its factory constructor."""
from irodsrulewrapper.dto.drop_zone import DropZone
from pydantic import BaseModel


class DropZones(BaseModel):
    """This class represents a list of iRODS DropZones DTOs."""

    drop_zones: list[DropZone]

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "DropZones":
        output = []
        for item in result:
            drop_zone = DropZone.create_from_rule_result(item)
            output.append(drop_zone)
        drop_zones = cls(drop_zones=output)

        return drop_zones
