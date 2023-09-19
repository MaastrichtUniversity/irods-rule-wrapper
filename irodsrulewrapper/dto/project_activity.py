"""This module contains the ProjectActivity DTO class and its factory constructors"""

from pydantic import BaseModel


class ProjectActivity(BaseModel):
    """This class represents the different activities related to a project. It is relevant for a project deletion"""

    has_process_activity: bool
    has_active_collection: bool

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "ProjectActivity":
        project_activity = cls(
            has_process_activity=result["has_process_activity"],
            has_active_collection=result["has_active_collection"],
        )

        return project_activity
