"""This module contains the ProjectsMinimal DTO class, its factory constructors and mock_json."""
import json

from pydantic import BaseModel

from irodsrulewrapper.dto.project_minimal import ProjectMinimal


class ProjectsMinimal(BaseModel):
    """
    This class represents a list of iRODS ProjectMinimal DTOs.
    it overwrites __iter__, __getitem__ & __len__ methods to make the ProjectsMinimal object behave like a list.
    """

    projects: list[ProjectMinimal]

    def __iter__(self):
        return iter(self.projects)

    def __getitem__(self, item):
        return self.projects[item]

    def __len__(self):
        return len(self.projects)

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "ProjectsMinimal":
        projects = []
        for item in result:
            project = ProjectMinimal.create_from_rule_result(item)
            projects.append(project)
        output = cls(projects=projects)
        return output

    @classmethod
    def create_from_mock_result(cls, projects_json=None) -> "ProjectsMinimal":
        if projects_json is None:
            projects_json = PROJECTS_MINIMAL_JSON
        return ProjectsMinimal.create_from_rule_result(json.loads(projects_json))


PROJECTS_MINIMAL_JSON: str = """
[
    {
        "id": "P000000010",
        "title": "(MDL) Placeholder project"
    },
    {
        "id": "P000000011",
        "title": "(HVC) Placeholder project"
    },
    {
        "id": "P000000012",
        "title": "Always the dullness of the fool is the whetstone of the wits."
    },
    {
        "id": "P000000013",
        "title": "You have a deep interest in all that is artistic."
    },
    {
        "id": "P000000014",
        "title": "You will be successful in love."
    },
    {
        "id": "P000000015",
        "title": "You will feel hungry again in another hour."
    },
    {
        "id": "P000000016",
        "title": "(ScaNxs) The lunatic, the lover, and the poet,"
    }
]
"""
