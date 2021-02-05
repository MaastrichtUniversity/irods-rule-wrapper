from .user import User


class Users:
    def __init__(self, users):
        self.users = users

    @classmethod
    def create_from_rule_result(cls, result):
        output = []
        for item in result:
            user = User.create_from_rule_result(item)
            output.append(user)
        users = cls(output)
        return users
