"""This module contains the ProjectContributorsMetadata DTO class and its factory constructor."""
import json

from dhpythonirodsutils.enums import ProjectAVUs

from irodsrulewrapper.dto.dto_base_model import DTOBaseModel
from irodsrulewrapper.dto.user_extended import UserExtended


class ProjectContributorsMetadata(DTOBaseModel):
    """
    This class represents the metadata contributor roles for an iRODS project.
    e.g: Data steward, Principal investigator ...
    """

    principal_investigator: UserExtended
    data_steward: UserExtended

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "ProjectContributorsMetadata":
        principal_investigator = UserExtended.create_from_rule_result(result["principalInvestigator"])
        data_steward = UserExtended.create_from_rule_result(result[ProjectAVUs.DATA_STEWARD.value])
        project = cls(principal_investigator=principal_investigator, data_steward=data_steward)

        return project

    @classmethod
    def create_from_mock_result(cls, mock_json=None) -> "ProjectContributorsMetadata":
        if mock_json is None:
            mock_json = CONTRIBUTORS_METADATA
        return ProjectContributorsMetadata.create_from_rule_result(json.loads(mock_json))


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
