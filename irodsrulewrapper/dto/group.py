class Group:
    def __init__(self, user_name, user_id, display_name, description):
        self.user_name = user_name
        self.user_id = user_id
        self.display_name = display_name
        self.description = description

    @classmethod
    def create_from_rule_result(cls, result):
        group = cls(result["userName"], result["userId"], result["displayName"], result["description"])
        return group
