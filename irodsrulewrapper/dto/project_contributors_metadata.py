import json

from typing import Dict

from irodsrulewrapper.dto.user_extended import UserExtended


class ProjectContributorsMetadata:
    def __init__(
        self,
        principal_investigator: UserExtended,
        data_steward: UserExtended,
    ):
        self.principal_investigator: UserExtended = principal_investigator
        self.data_steward: UserExtended = data_steward

    @classmethod
    def create_from_rule_result(cls, result: Dict) -> "ProjectContributorsMetadata":
        principal_investigator = UserExtended.create_from_rule_result(result["principalInvestigator"])
        data_steward = UserExtended.create_from_rule_result(result["dataSteward"])
        project = cls(principal_investigator, data_steward)

        return project

    @classmethod
    def create_from_mock_result(cls, project_json=None) -> "ProjectContributorsMetadata":
        if project_json is None:
            project_json = cls.CONTRIBUTORS_METADATA
        return ProjectContributorsMetadata.create_from_rule_result(json.loads(project_json))

    CONTRIBUTORS_METADATA = """
    {
        "dataSteward": {
            "displayName": "Olav Palmen",
            "email": "o.palmen@maastrichtuniversity.nl",
            "familyName": "Palmen",
            "givenName": "Olav",
            "username": "opalmen"
        },
        "principalInvestigator": {
            "displayName": "Pascal Suppers",
            "email": "p.suppers@maastrichtuniversity.nl",
            "familyName": "Suppers",
            "givenName": "Pascal",
            "username": "psuppers"
        }
    }
    """
