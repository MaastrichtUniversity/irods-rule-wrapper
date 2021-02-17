class Project:
    def __init__(self, project, resource, title, pi, responsible_cost_center, storage_quota_gb, data_steward):
        self.project = project
        self.resource = resource
        self.title = title
        self.pi = pi
        self.responsible_cost_center = responsible_cost_center
        self.storage_quota_gb = storage_quota_gb
        self.data_steward = data_steward

    @classmethod
    def create_from_rule_result(cls, result):
        Project = cls(result["project"], result["resource"], result["title"], result["principalInvestigator"], result["respCostCenter"], result["storageQuotaGiB"], result["dataSteward"])
        return Project
