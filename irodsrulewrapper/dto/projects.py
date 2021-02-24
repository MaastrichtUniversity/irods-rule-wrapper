from .project import Project
from typing import List, Dict


class Projects:
    def __init__(self, projects: List['Project'], has_financial_view_access: bool):
        self.projects: List['Project'] = projects
        self.has_financial_view_access: bool = has_financial_view_access

    @classmethod
    def create_from_rule_result(cls, result: Dict) -> 'Projects':
        output = []
        for item in result['projects']:
            project = Project.create_from_rule_result(item)
            output.append(project)
        projects = cls(output, result['has_financial_view_access'])
        return projects
