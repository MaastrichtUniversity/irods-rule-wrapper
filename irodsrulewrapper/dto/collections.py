"""This module contains the Collections DTO class and its factory constructor."""
import json

from irodsrulewrapper.dto.collection import Collection
from irodsrulewrapper.dto.dto_base_model import DTOBaseModel


class Collections(DTOBaseModel):
    """This class represents a list of iRODS Collection DTOs."""

    collections: list[Collection]

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "Collections":
        collections = []
        for item in result:
            collection = Collection.create_from_rule_result(item)
            collections.append(collection)
        output = cls(collections=collections)
        return output

    @classmethod
    def create_from_mock_result(cls, mock_json=None) -> "Collections":
        if mock_json is None:
            mock_json = COLLECTIONS_JSON
        return Collections.create_from_rule_result(json.loads(mock_json))


COLLECTIONS_JSON = """
[
    {
        "PID": "21.T12996/P000000010C000000001",
        "creator": "jonathan.melius@maastrichtuniversity.nl",
        "id": "C000000001",
        "numFiles": "1253",
        "numUserFiles": 1251,
        "size": 2793.9677238464355,
        "title": "Test Coll 1"
    },
    {
        "PID": "21.T12996/P000000010C000000002",
        "creator": "jonathan.melius@maastrichtuniversity.nl",
        "id": "C000000002",
        "numFiles": "42",
        "numUserFiles": 40,
        "size": 0.0,
        "title": "Test Coll 2.0"
    }
]
"""
