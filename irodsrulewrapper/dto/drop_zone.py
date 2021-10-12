from typing import Dict


class DropZone:
    def __init__(
        self,
        date: str,
        project: str,
        project_title: str,
        state: str,
        title: str,
        token: str,
        validate_msg: str,
        validate_state: str,
        resource_status: str,
        total_size: str,
        destination: str,
    ):
        self.date: str = date
        self.project: str = project
        self.project_title: str = project_title
        self.state: str = state
        self.title: str = title
        self.token: str = token
        self.validate_msg: str = validate_msg
        self.validate_state: str = validate_state
        self.resource_status: str = resource_status
        self.total_size: str = total_size
        self.destination: str = destination

    @classmethod
    def create_from_rule_result(cls, result: Dict) -> "DropZone":
        if "resourceStatus" not in result:
            result["resourceStatus"] = ""

        user = cls(
            result["date"],
            result["project"],
            result["projectTitle"],
            result["state"],
            result["title"],
            result["token"],
            result["validateMsg"],
            result["validateState"],
            result["resourceStatus"],
            result["totalSize"],
            result["destination"],
        )
        return user
