"""This module contains the Users DTO class, its factory constructors and mock_json."""
import json

from irodsrulewrapper.dto.group import Group
from pydantic import BaseModel
from typing import List


class Groups(BaseModel):
    """This class represents a list of iRODS Group DTOs."""

    groups: List[Group]

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "Groups":
        output = []
        for item in result:
            group = Group.create_from_rule_result(item)
            output.append(group)
        groups = cls(groups=output)
        return groups

    @classmethod
    def create_from_mock_result(cls, mock_json=None) -> "Groups":
        if mock_json is None:
            mock_json = MOCK_JSON
        return cls.create_from_rule_result(json.loads(mock_json))


MOCK_JSON = """
[
    {
        "description": "CO for PhD project of P7000815",
        "displayName": "Novel approach for smashing ions",
        "groupId": "10199",
        "name": "m4i-nanoscopy-phd0815"
    },
    {
        "description": "CO for all of nanoscopy",
        "displayName": "Nanoscopy",
        "groupId": "10124",
        "name": "m4i-nanoscopy"
    },
    {
        "description": "UM-SCANNEXUS",
        "displayName": "SCANNEXUS",
        "groupId": "10133",
        "name": "scannexus"
    },
    {
        "description": "It's DataHub! The place to store your data.",
        "displayName": "DataHub",
        "groupId": "10127",
        "name": "datahub"
    },
    {
        "description": "",
        "displayName": "m4i-massspec",
        "groupId": "10192",
        "name": "m4i-massspec"
    }
]

"""
