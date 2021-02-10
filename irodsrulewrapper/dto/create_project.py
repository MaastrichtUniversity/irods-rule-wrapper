class CreateProject:
    def __init__(self, project_path, project_id):
        self.project_path = project_path
        self.project_id = project_id

    @classmethod
    def create_from_rule_result(cls, result):
        project = cls(result["project_path"], result["project_id"])
        return project
