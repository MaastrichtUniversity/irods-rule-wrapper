from .group import Group
from typing import List, Dict


class Groups:
    def __init__(self, groups: List['Group']):
        self.groups: List['Group'] = groups

    @classmethod
    def create_from_rule_result(cls, result: Dict) -> 'DataStewards':
        output = []
        for item in result:
            group = Group.create_from_rule_result(item)
            output.append(group)
        groups = cls(output)
        return groups
