import json

import pytest
from pydantic import ValidationError

from irodsrulewrapper.dto.drop_zone import DropZone
from irodsrulewrapper.dto.drop_zones import DropZones
from irodsrulewrapper.dto.token import Token


def test_dto_dropzone():
    dropzone = DropZone.create_from_rule_result(json.loads(DROPZONE))
    assert dropzone.state == "error-post-ingestion"


@pytest.mark.parametrize(
    "total_size, expected",
    [(0, "0"), (521844260, "521844260"), (521844260.0, "521844260.0"), ("0", "0"), ("521844260", "521844260")],
)
def test_dto_dropzone_total_size(total_size, expected):
    result = json.loads(DROPZONE)
    result["totalSize"] = total_size

    dropzone = DropZone.create_from_rule_result(result)
    assert dropzone.total_size == expected
    assert dropzone.model_dump()["total_size"] == expected
    assert DropZones.create_from_rule_result([result]).drop_zones[0].total_size == expected

    model_data = dropzone.model_dump()
    model_data["total_size"] = total_size
    assert DropZone.model_validate(model_data).total_size == expected


@pytest.mark.parametrize("total_size", [None, True, [], {}])
def test_dto_dropzone_rejects_invalid_total_size(total_size):
    result = json.loads(DROPZONE)
    result["totalSize"] = total_size

    with pytest.raises(ValidationError) as error:
        DropZone.create_from_rule_result(result)

    assert error.value.errors()[0]["loc"] == ("total_size",)


@pytest.mark.parametrize(
    "sharing, expected", [(True, True), (False, False), ("true", True), ("false", False), ("", False)]
)
def test_dto_dropzone_sharing_flags(sharing, expected):
    result = json.loads(DROPZONE)
    result["sharedWithMe"] = sharing
    result["enableDropzoneSharing"] = sharing

    dropzone = DropZone.create_from_rule_result(result)

    assert dropzone.shared_with_me is expected
    assert dropzone.dropzone_sharing_enabled is expected


@pytest.mark.parametrize("state", ["in-queue-for-validation", "in-queue-for-maintenance-end"])
def test_dto_dropzone_preserves_queued_state(state):
    result = json.loads(DROPZONE)
    result["state"] = state

    dropzone = DropZone.create_from_rule_result(result)
    assert dropzone.state == state
    assert dropzone.model_dump()["state"] == state
    assert json.loads(dropzone.model_dump_json())["state"] == state
    assert DropZones.create_from_rule_result([result]).drop_zones[0].state == state


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
    "percentage_ingested": 100.0,
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
    "percentage_ingested": 0.0,
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
    "percentage_ingested": 50.0,
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
