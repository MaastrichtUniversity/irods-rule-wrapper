class ProjectCost:
    def __init__(self, project_id, project_cost_yearly, project_cost_monthly,
                 project_size_gb, project_size_gib, budget_number, title):
        self.project_id = project_id
        self.project_cost_yearly = project_cost_yearly
        self.project_cost_monthly = project_cost_monthly
        self.project_size_gb = project_size_gb
        self.project_size_gib = project_size_gib
        self.budget_number = budget_number
        self.title = title

    @classmethod
    def create_from_rule_result(cls, result):
        user = cls(result["project_id"], result["project_cost_monthly"], result["project_cost_yearly"],
                   result["project_size_gb"], result["project_size_gib"],
                   result["budget_number"], result["title"])
        return user
