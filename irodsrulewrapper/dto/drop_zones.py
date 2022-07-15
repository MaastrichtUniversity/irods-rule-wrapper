from irodsrulewrapper.dto.drop_zone import DropZone


class DropZones:
    def __init__(self, users: list["DropZone"]):
        self.drop_zones: list["DropZone"] = users

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "DropZones":
        output = []
        for item in result:
            drop_zone = DropZone.create_from_rule_result(item)
            output.append(drop_zone)
        drop_zones = cls(output)
        return drop_zones
