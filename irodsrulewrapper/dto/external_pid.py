"""This module contains the ExternalPID class and its factory constructor."""
from irodsrulewrapper.dto.dto_base_model import DTOBaseModel


class ExternalPID(DTOBaseModel):
    """This class represents an external PID link"""

    pid: str
    repository: str

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "ExternalPID":
        pid = "https://doi.org/" + result["value"].split(":")[1]
        user = cls(pid=pid, repository=result["unit"])
        return user
