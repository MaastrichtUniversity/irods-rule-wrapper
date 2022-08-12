"""This module contains the CreateProject DTO class and its factory constructor."""
from irodsrulewrapper.dto.dto_base_model import DTOBaseModel


class CreateProject(DTOBaseModel):
    """This class represents newly created iRODS project with minimal attributes"""

    project_path: str
    project_id: str

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "CreateProject":
        project = cls(project_path=result["project_path"], project_id=result["project_id"])
        return project
