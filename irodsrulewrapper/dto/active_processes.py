"""This module contains the ActiveProcesses DTO class and its factory constructor."""
from irodsrulewrapper.dto.active_proces import ActiveProcess
from irodsrulewrapper.dto.drop_zone import DropZone


class ActiveProcesses:
    """
    This class represents a list of iRODS active data transfer processes (ingest, tape archive & DataverseNL export).
    """

    def __init__(
        self,
        dropzones: list["DropZone"],
        exports: list["ActiveProcess"],
        archives: list["ActiveProcess"],
        unarchives: list["ActiveProcess"],
    ):
        self.drop_zones: list["DropZone"] = dropzones
        self.exports: list["ActiveProcess"] = exports
        self.archives: list["ActiveProcess"] = archives
        self.unarchives: list["ActiveProcess"] = unarchives

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
        unarchives = []
        for unarchive_item in result["unarchive"]:
            unarchive = ActiveProcess.create_from_rule_result(unarchive_item)
            unarchives.append(unarchive)
        exports = []
        for export_item in result["export"]:
            export = ActiveProcess.create_from_rule_result(export_item)
            exports.append(export)
        output = cls(dropzones, exports, archives, unarchives)
        return output
