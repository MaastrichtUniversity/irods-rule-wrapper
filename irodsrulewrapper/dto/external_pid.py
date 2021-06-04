from typing import Dict


class ExternalPID:
    def __init__(self, pid: str, repository: str):
        self.pid: str = pid
        self.repository: str = repository

    @classmethod
    def create_from_rule_result(cls, result: Dict) -> 'ExternalPID':
        user = cls(result["value"], result["unit"])
        return user
