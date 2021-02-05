class User:
    def __init__(self, user_name, user_id, display_name):
        self.user_name = user_name
        self.user_id = user_id
        self.display_name = display_name

    @classmethod
    def create_from_rule_result(cls, result):
        user = cls(result["userName"], result["userId"], result["displayName"])
        return user
