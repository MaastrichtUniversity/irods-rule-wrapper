from typing import Dict


class ProjectContributorsMetadata:
    def __init__(
        self,
        principal_investigator: str,
        principal_investigator_display_name: str,
        principal_investigator_given_name: str,
        principal_investigator_family_name: str,
        principal_investigator_email: str,
        data_steward: str,
        data_steward_display_name: str,
        data_steward_given_name: str,
        data_steward_family_name: str,
        data_steward_email: str,
    ):
        self.principal_investigator: str = principal_investigator
        self.principal_investigator_display_name: str = principal_investigator_display_name
        self.principal_investigator_given_name: str = principal_investigator_given_name
        self.principal_investigator_family_name: str = principal_investigator_family_name
        self.principal_investigator_email: str = principal_investigator_email
        self.data_steward: str = data_steward
        self.data_steward_display_name: str = data_steward_display_name
        self.data_steward_given_name: str = data_steward_given_name
        self.data_steward_family_name: str = data_steward_family_name
        self.data_steward_email: str = data_steward_email

    @classmethod
    def create_from_rule_result(cls, result: Dict) -> "ProjectContributorsMetadata":
        project = cls(
            result["principalInvestigator"],
            result["principalInvestigatorDisplayName"],
            result["principalInvestigatorGivenName"],
            result["principalInvestigatorFamilyName"],
            result["principalInvestigatorEmail"],
            result["dataSteward"],
            result["dataStewardDisplayName"],
            result["dataStewardGivenName"],
            result["dataStewardFamilyName"],
            result["dataStewardEmail"],
        )
        return project
