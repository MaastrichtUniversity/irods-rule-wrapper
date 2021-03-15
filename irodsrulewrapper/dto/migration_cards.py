from .migration_card import MigrationCard
from typing import List, Dict


class MigrationCards:
    def __init__(self, cards: List['MigrationCard']):
        self.cards: List['MigrationCard'] = cards

    @classmethod
    def create_from_rule_result(cls, result: Dict) -> 'MigrationCards':
        output = []
        for item in result:
            card = MigrationCard.create_from_rule_result(item)
            output.append(card)
        cards = cls(output)
        return cards
