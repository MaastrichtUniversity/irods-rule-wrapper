from .project import Project


class Projects:
    def __init__(self, projects):
        self.projects = projects

    @classmethod
    def create_from_rule_result(cls, result):
        output = []
        for item in result:
            project = Project.create_from_rule_result(item)
            output.append(project)
        projects = cls(output)
        return projects
