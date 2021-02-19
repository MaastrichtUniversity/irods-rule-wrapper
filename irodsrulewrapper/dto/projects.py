from .project import Project
from typing import List, Dict


class Projects:
    def __init__(self, projects: List['Project']):
        self.projects: List['Project'] = projects

    @classmethod
    def create_from_rule_result(cls, result: Dict) -> 'Projects':
        output = []
        for item in result:
            project = Project.create_from_rule_result(item)
            output.append(project)
        projects = cls(output)
        return projects
