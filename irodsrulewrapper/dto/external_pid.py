"""This module contains the ExternalPID class and its factory constructor."""


class ExternalPID:
    """This class represents an external PID link"""

    def __init__(self, pid: str, repository: str):
        self.pid: str = pid
        self.repository: str = repository

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "ExternalPID":
        pid = "https://doi.org/" + result["value"].split(":")[1]
        user = cls(pid, result["unit"])
        return user
