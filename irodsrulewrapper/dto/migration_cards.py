from irodsrulewrapper.dto.migration_card import MigrationCard


class MigrationCards:
    def __init__(self, cards: list["MigrationCard"]):
        self.cards: list["MigrationCard"] = cards

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "MigrationCards":
        output = []
        for item in result:
            card = MigrationCard.create_from_rule_result(item)
            output.append(card)
        cards = cls(output)
        return cards
