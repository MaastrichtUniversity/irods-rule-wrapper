"""This module contains the ProjectsOverview DTO class and its factory constructor."""
from irodsrulewrapper.cache import CacheTTL
from irodsrulewrapper.dto.project_overview import ProjectOverview


class ProjectsOverview:
    """
    This class represents a list of iRODS ProjectsOverview DTOs.
    """

    def __init__(self, projects: list["ProjectOverview"]):
        self.projects: list["ProjectOverview"] = projects

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "ProjectsOverview":
        CacheTTL.check_if_cache_expired()
        output = []
        for item in result:
            project = ProjectOverview.create_from_rule_result(
                item,
            )
            output.append(project)
        projects = cls(output)
        return projects
