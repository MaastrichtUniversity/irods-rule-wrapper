"""This module contains the ContributingProjects DTO class and its factory constructor."""
from irodsrulewrapper.dto.contributing_project import ContributingProject


class ContributingProjects:
    """This class represents a list of iRODS ContributingProject DTOs."""

    def __init__(self, projects: list["ContributingProject"]):
        self.projects: list["ContributingProject"] = projects

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "ContributingProject":
        # get_contributing_projects returns an empty list, if the user is not a contributor for the project
        if len(result) == 0:
            return None

        output = []
        for item in result:
            drop_zone = ContributingProject.create_from_rule_result(item)
            output.append(drop_zone)
        projects = cls(output)
        return projects
