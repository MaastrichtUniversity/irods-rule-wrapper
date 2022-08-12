"""This module contains the MigrationCards DTO class and its factory constructor."""
import json

from irodsrulewrapper.dto.dto_base_model import DTOBaseModel
from irodsrulewrapper.dto.migration_card import MigrationCard


class MigrationCards(DTOBaseModel):
    """This class represents a list of MigrationCard User DTOs."""

    cards: list[MigrationCard]

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "MigrationCards":
        output = []
        for item in result:
            card = MigrationCard.create_from_rule_result(item)
            output.append(card)
        cards = cls(cards=output)
        return cards

    @classmethod
    def create_from_mock_result(cls, mock_json=None) -> "MigrationCards":
        if mock_json is None:
            mock_json = MIGRATION_CARDS
        return MigrationCards.create_from_rule_result(json.loads(mock_json))


MIGRATION_CARDS = """
[
  {
    "status": "archive-done",
    "repository": "SURFSara Tape",
    "collection": "C000000001",
    "title": "Test 1"
  },
  {
    "status": "in-queue-for-export",
    "repository": "DataverseNL",
    "collection": "C000000001",
    "title": "Test 1"
  }
]
"""
