from irodsrulewrapper.dto.data_steward import DataSteward


class DataStewards:
    def __init__(self, data_stewards: list["DataSteward"]):
        self.data_stewards: list["DataSteward"] = data_stewards

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "DataStewards":
        output = []
        for item in result:
            user = DataSteward.create_from_rule_result(item)
            output.append(user)
        data_stewards = cls(output)
        return data_stewards
