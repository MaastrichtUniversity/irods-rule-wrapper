"""This module contains the ProjectContributorsMetadata DTO class and its factory constructor."""
import json

from dhpythonirodsutils.enums import ProjectAVUs

from irodsrulewrapper.dto.user_extended import UserExtended


class ProjectContributorsMetadata:
    """
    This class represents the metadata contributor roles for an iRODS project.
    e.g: Data steward, Principal investigator ...
    """

    def __init__(
        self,
        principal_investigator: UserExtended,
        data_steward: UserExtended,
    ):
        self.principal_investigator: UserExtended = principal_investigator
        self.data_steward: UserExtended = data_steward

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "ProjectContributorsMetadata":
        principal_investigator = UserExtended.create_from_rule_result(result["principalInvestigator"])
        data_steward = UserExtended.create_from_rule_result(result[ProjectAVUs.DATA_STEWARD.value])
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
            "email": "o.pa@maastrichtuniversity.nl",
            "familyName": "Palmen",
            "givenName": "Olav",
            "username": "opalmen"
        },
        "principalInvestigator": {
            "displayName": "Pascal Suppers",
            "email": "p.sups@maastrichtuniversity.nl",
            "familyName": "Suppers",
            "givenName": "Pascal",
            "username": "psuppers"
        }
    }
    """
