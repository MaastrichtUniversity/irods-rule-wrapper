from typing import Dict


class DropZone:
    def __init__(self, date: str, project: str, project_title: str,
                 state: str, title: str, token: str, validate_msg: str, validate_state: str):
        self.date: str = date
        self.project: str = project
        self.project_title: str = project_title
        self.state: str = state
        self.title: str = title
        self.token: str = token
        self.validate_msg: str = validate_msg
        self.validate_state: str = validate_state

    @classmethod
    def create_from_rule_result(cls, result: Dict) -> 'DropZone':
        user = cls(result["date"], result["project"], result["projectTitle"], result["state"], result["title"],
                   result["token"], result["validateMsg"], result["validateState"])
        return user
