from typing import List, Dict


class ContributingProject:
    def __init__(self, id: str, title: str, managers: List[str], contributors: List[str], viewers: List[str]):
        self.id: str = id
        self.title: str = title
        self.managers: List[str] = managers
        self.contributors: List[str] = contributors
        self.viewers: List[str] = viewers

    @classmethod
    def create_from_rule_result(cls, result: Dict) -> 'ManagingProjects':
        managers = result["managers"]["users"]
        contributors = result["contributors"]["users"] + result["contributors"]["groups"]
        viewers = result["viewers"]["users"] + result["viewers"]["groups"]
        projects = cls(result["id"], result["title"], managers, contributors, viewers)

        return projects
