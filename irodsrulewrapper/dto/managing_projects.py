class ManagingProjects:
    def __init__(self, managers, contributors, viewers):
        self.managers = managers
        self.contributors = contributors
        self.viewers = viewers

    @classmethod
    def create_from_rule_result(cls, result):
        # get_managing_project returns an empty list, if the user is not a manager for the project
        if len(result) == 0:
            return None

        managers = result["managers"]["users"]
        contributors = result["contributors"]["users"] + result["contributors"]["groups"]
        viewers = result["viewers"]["users"] + result["viewers"]["groups"]
        projects = cls(managers, contributors, viewers)

        return projects
