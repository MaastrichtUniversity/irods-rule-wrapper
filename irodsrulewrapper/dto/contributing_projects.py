from .contributing_project import ContributingProject
from typing import List, Dict


class ContributingProjects:
    def __init__(self, projects: List["ContributingProject"]):
        self.projects: List["ContributingProject"] = projects

    @classmethod
    def create_from_rule_result(cls, result: Dict) -> "ContributingProject":
        # get_contributing_projects returns an empty list, if the user is not a contributor for the project
        if len(result) == 0:
            return None

        output = []
        for item in result:
            drop_zone = ContributingProject.create_from_rule_result(item)
            output.append(drop_zone)
        projects = cls(output)
        return projects
