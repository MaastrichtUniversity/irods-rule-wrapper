from .project_cost import ProjectCost
from typing import List, Dict


class ProjectsCost:
    def __init__(self, projects_cost: List['ProjectCost']):
        self.projects_cost: List['ProjectCost'] = projects_cost

    @classmethod
    def create_from_rule_result(cls, result: Dict) -> 'ProjectsCost':
        # get_projects_finance returns an empty list, if the user is not the PI or data steward of the project
        if len(result) == 0:
            return None

        output = []
        for item in result:
            project = ProjectCost.create_from_rule_result(item)
            output.append(project)
        projects = cls(output)
        return projects
