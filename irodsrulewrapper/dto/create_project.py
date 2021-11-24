from typing import Dict


class CreateProject:
    def __init__(self, project_path: str, project_id: str):
        self.project_path: str = project_path
        self.project_id: str = project_id

    @classmethod
    def create_from_rule_result(cls, result: Dict) -> "CreateProject":
        project = cls(result["project_path"], result["project_id"])
        return project
