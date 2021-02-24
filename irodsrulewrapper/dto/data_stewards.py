from .data_steward import DataSteward
from typing import List, Dict


class DataStewards:
    def __init__(self, data_stewards: List['DataSteward']):
        self.data_stewards: List['DataSteward'] = data_stewards

    @classmethod
    def create_from_rule_result(cls, result: Dict) -> 'DataStewards':
        output = []
        for item in result:
            user = DataSteward.create_from_rule_result(item)
            output.append(user)
        data_stewards = cls(output)
        return data_stewards
