from irodsrulewrapper.dto.active_proces import ActiveProcess
from irodsrulewrapper.dto.drop_zone import DropZone


class ActiveProcesses:
    def __init__(self, dropzones: list["DropZone"], exports: list["ActiveProces"], archives: list["ActiveProces"]):
        self.drop_zones: list["DropZone"] = dropzones
        self.exports: list["ActiveProces"] = exports
        self.archives: list["ActiveProces"] = archives

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "ActiveProcesses":
        dropzones = []
        for drop_zone_item in result["drop_zones"]:
            drop_zone = DropZone.create_from_rule_result(drop_zone_item)
            dropzones.append(drop_zone)
        archives = []
        for archive_item in result["archive"]:
            archive = ActiveProcess.create_from_rule_result(archive_item)
            archives.append(archive)
        exports = []
        for export_item in result["export"]:
            export = ActiveProcess.create_from_rule_result(export_item)
            exports.append(export)
        output = cls(dropzones, exports, archives)
        return output
