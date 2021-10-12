class ProjectCost:
    def __init__(
        self,
        project_id: str,
        project_cost_yearly: float,
        project_cost_monthly: float,
        project_size_gb: float,
        project_size_gib: float,
        budget_number: str,
        title: str,
    ):
        self.project_id: str = project_id
        self.project_cost_yearly: float = project_cost_yearly
        self.project_cost_monthly: float = project_cost_monthly
        self.project_size_gb: float = project_size_gb
        self.project_size_gib: float = project_size_gib
        self.budget_number: str = budget_number
        self.title: str = title

    @classmethod
    def create_from_rule_result(cls, result):
        user = cls(
            result["project_id"],
            result["project_cost_yearly"],
            result["project_cost_monthly"],
            result["project_size_gb"],
            result["project_size_gib"],
            result["budget_number"],
            result["title"],
        )
        return user
