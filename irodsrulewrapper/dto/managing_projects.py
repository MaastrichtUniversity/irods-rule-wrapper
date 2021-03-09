from typing import List, Dict


class ManagingProjects:
    def __init__(self, managers: List[str], contributors: List[str], viewers: List[str],
                 principal_investigator: str, data_steward: str):
        self.managers: List[str] = managers
        self.contributors: List[str] = contributors
        self.viewers: List[str] = viewers
        self.principal_investigator: str = principal_investigator
        self.data_steward: str = data_steward

    @classmethod
    def create_from_rule_result(cls, result: Dict) -> 'ManagingProjects':
        # get_managing_projects returns an empty list, if the user is not a manager for the project
        if len(result) == 0:
            return None

        managers = result["managers"]["users"]
        contributors = result["contributors"]["users"] + result["contributors"]["groups"]
        viewers = result["viewers"]["users"] + result["viewers"]["groups"]
        projects = cls(managers, contributors, viewers, result["principal_investigator"], result["data_steward"])

        return projects
