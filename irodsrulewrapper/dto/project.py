from typing import Dict


class Project:
    def __init__(self,
                 project: str,
                 resource: str,
                 title: str,
                 principle_investigator: str,
                 responsible_cost_center: str,
                 storage_quota_gb: int,
                 data_steward: str):
        self.project = project
        self.resource: str = resource
        self.title: str = title
        self.principle_investigator: str = principle_investigator
        self.responsible_cost_center: str = responsible_cost_center
        self.storage_quota_gb: int = storage_quota_gb
        self.data_steward: str = data_steward

    @classmethod
    def create_from_rule_result(cls, result: Dict):
        project = cls(result["project"],
                      result["resource"],
                      result["title"],
                      result["principalInvestigator"],
                      result["respCostCenter"],
                      result["storageQuotaGiB"],
                      result["dataSteward"])
        return project
