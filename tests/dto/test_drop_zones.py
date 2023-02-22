import json

from irodsrulewrapper.dto.drop_zone import DropZone
from irodsrulewrapper.dto.drop_zones import DropZones
from irodsrulewrapper.dto.token import Token


def test_dto_dropzone():
    dropzone = DropZone.create_from_rule_result(json.loads(DROPZONE))
    assert dropzone.state == "error-post-ingestion"


def test_dto_dropzones():
    dropzones = DropZones.create_from_rule_result(json.loads(DROPZONES)).drop_zones
    assert dropzones[0].state == "open"


def test_dto_token():
    ret = Token.create_from_rule_result(json.loads('"token"'))
    assert ret.token == "token"


DROPZONE = """
  {
    "totalSize": "521844260",
    "token": "prickly-caracal",
    "type": "mounted",
    "process_type": "drop_zone",
    "sharedWithMe": "true",
    "state": "error-post-ingestion",
    "validateMsg": "N/A",
    "project": "P000000014",
    "title": "Test sprint 1",
    "validateState": "N/A",
    "projectTitle": "Hope that the day after you die is a nice day.",
    "enableDropzoneSharing": "true",
    "date": "01659701010",
    "creator": "jmelius",
    "destination": "C000000001",
    "startDate": "2022-08-05",
    "userName": "N/A",
    "endDate": "2022-11-03"
  }
"""

DROPZONES = """
[
  {
    "totalSize": "521844260",
    "token": "prickly-caracal",
    "type": "mounted",
    "process_type": "drop_zone",
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
    "process_type": "drop_zone",
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
