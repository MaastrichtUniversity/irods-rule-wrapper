"""This module contains the ContributingProjects DTO class and its factory constructor."""
from irodsrulewrapper.dto.contributing_project import ContributingProject

from pydantic import BaseModel
from typing import List


class ContributingProjects(BaseModel):
    """This class represents a list of iRODS ContributingProject DTOs."""

    projects: List[ContributingProject]

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "ContributingProject":
        # get_contributing_projects returns an empty list, if the user is not a contributor for the project
        if len(result) == 0:
            return None

        output = []
        for item in result:
            project = ContributingProject.create_from_rule_result(item)
            output.append(project)
        projects = cls(projects=output)
        return projects
