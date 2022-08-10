"""This module contains the DropZones class and its factory constructor."""
import json

from irodsrulewrapper.dto.drop_zone import DropZone


class DropZones:
    """This class represents a list of iRODS DropZones DTOs."""

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

    @classmethod
    def create_from_mock_result(cls, mock_json=None) -> "DropZones":
        if mock_json is None:
            mock_json = DROPZONES
        return DropZones.create_from_rule_result(json.loads(mock_json))


DROPZONES = """
[
  {
    "totalSize": "521844260",
    "token": "prickly-caracal",
    "type": "mounted",
    "sharedWithMe": "true",
    "state": "open",
    "validateMsg": "N/A",
    "project": "P000000014",
    "title": "Test sprint 1",
    "validateState": "N/A",
    "projectTitle": "You recoil from the crude; you tend naturally toward the exquisite.",
    "enableDropzoneSharing": "true",
    "date": "01659701010",
    "creator": "jmelius",
    "destination": "C000000001",
    "startDate": "2022-08-05",
    "userName": "N/A",
    "endDate": "2022-11-03"
  },
   {
    "totalSize": "123456789",
    "token": "crazy-frog",
    "type": "direct",
    "sharedWithMe": "true",
    "state": "error-post-ingestion",
    "validateMsg": "N/A",
    "project": "P000000014",
    "title": "Test sprint 1",
    "validateState": "N/A",
    "projectTitle": "You recoil from the crude; you tend naturally toward the exquisite.",
    "enableDropzoneSharing": "true",
    "date": "01659701010",
    "creator": "jmelius",
    "destination": "C000000002",
    "startDate": "2022-08-05",
    "userName": "N/A",
    "endDate": "2022-11-03"
  }
]
"""
