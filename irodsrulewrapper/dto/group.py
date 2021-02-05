class Group:
    def __init__(self, user_name, user_id, display_name, description):
        self.user_name = user_name
        self.user_id = user_id
        self.display_name = display_name
        self.description = description

    @classmethod
    def create_from_rule_result(cls, group):
        group = cls(group["userName"], group["userId"], group["displayName"], group["description"])
        return group
