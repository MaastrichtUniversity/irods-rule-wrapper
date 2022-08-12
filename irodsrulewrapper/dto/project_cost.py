"""This module contains the ProjectCost DTO class and its factory constructor."""
from irodsrulewrapper.dto.dto_base_model import DTOBaseModel


class ProjectCost(DTOBaseModel):
    """This class represents the cost information for an iRODS project."""

    project_id: str
    project_cost_yearly: float
    project_cost_monthly: float
    project_size_gb: float
    project_size_gib: float
    budget_number: str
    title: str

    @classmethod
    def create_from_rule_result(cls, result):
        user = cls(
            project_id=result["project_id"],
            project_cost_yearly=result["project_cost_yearly"],
            project_cost_monthly=result["project_cost_monthly"],
            project_size_gb=result["project_size_gb"],
            project_size_gib=result["project_size_gib"],
            budget_number=result["budget_number"],
            title=result["title"],
        )
        return user
