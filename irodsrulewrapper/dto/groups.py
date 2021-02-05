class Groups:
    def __init__(self, groups, group_objects):
        self.groups = groups
        self.groupObject = group_objects

    @classmethod
    def create_from_rule_result(cls, result):
        groups = cls(result['groups'], result['group_objects'])
        return groups
