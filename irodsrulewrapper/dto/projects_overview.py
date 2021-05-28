from .project_overview import ProjectOverview
from typing import List, Dict


class ProjectsOverview:
    def __init__(self, projects: List['ProjectOverview'], has_financial_view_access: bool):
        self.projects: List['ProjectOverview'] = projects
        self.has_financial_view_access: bool = has_financial_view_access

    @classmethod
    def create_from_rule_result(cls, result: Dict) -> 'ProjectsOverview':
        output = []
        for item in result:
            project = ProjectOverview.create_from_rule_result(item)
            output.append(project)
        projects = cls(output, False) #result['has_financial_view_access']
        return projects
