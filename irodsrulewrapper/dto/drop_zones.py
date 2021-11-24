from .drop_zone import DropZone
from typing import List, Dict


class DropZones:
    def __init__(self, users: List["DropZone"]):
        self.drop_zones: List["DropZone"] = users

    @classmethod
    def create_from_rule_result(cls, result: Dict) -> "DropZone":
        output = []
        for item in result:
            drop_zone = DropZone.create_from_rule_result(item)
            output.append(drop_zone)
        drop_zones = cls(output)
        return drop_zones
