from .data_steward import DataSteward


class DataStewards:
    def __init__(self, data_stewards):
        self.data_stewards = data_stewards

    @classmethod
    def create_from_rule_result(cls, result):
        output = []
        for item in result:
            user = DataSteward.create_from_rule_result(item)
            output.append(user)
        data_stewards = cls(output)
        return data_stewards
