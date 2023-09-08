"""This module contains the Users DTO class and its factory constructors"""

from pydantic import BaseModel


class ProjectActivity(BaseModel):
    """This class represents a list of iRODS Group DTOs."""

    has_active_drop_zones: bool
    has_active_processes: bool
    has_pending_deletions: bool

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "ProjectActivity":
        project_activity = cls(
            has_active_drop_zones=result["has_active_drop_zones"],
            has_active_processes=result["has_active_processes"],
            has_pending_deletions=result["has_pending_deletions"],
        )

        return project_activity
