class Group:
    def __init__(self, name, group_id, display_name, description):
        self.name = name
        self.id = group_id
        self.display_name = display_name
        self.description = description

    @classmethod
    def create_from_rule_result(cls, result):
        # Backward compatibility
        name = ''
        if "userName" in result:
            name = result["userName"]
        elif "name" in result:
            name = result["name"]
        group_id = ''
        if "userId" in result:
            group_id = result["userId"]
        elif "groupId" in result:
            group_id = result["groupId"]

        group = cls(name, group_id, result["displayName"], result["description"])
        return group
