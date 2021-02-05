from .group import Group


class Groups:
    def __init__(self, groups):
        self.groups = groups

    @classmethod
    def create_from_rule_result(cls, result):
        output = []
        for item in result:
            group = Group.create_from_rule_result(item)
            output.append(group)
        groups = cls(output)
        return groups
