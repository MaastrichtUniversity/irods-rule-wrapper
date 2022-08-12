"""This module contains the TapeEstimate DTO class and its factory constructor."""
from irodsrulewrapper.dto.dto_base_model import DTOBaseModel


class TapeEstimate(DTOBaseModel):
    """This class represents the tape archival estimation information for an IRODS project collection."""

    above_threshold_bytes_size: int
    above_threshold_number_files: int
    archivable_bytes_size: int
    archivable_number_files: int
    status: str

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "TapeEstimate":
        group = cls(
            above_threshold_bytes_size=result["above_threshold"]["bytes_size"],
            above_threshold_number_files=result["above_threshold"]["number_files"],
            archivable_bytes_size=result["archivable"]["bytes_size"],
            archivable_number_files=result["archivable"]["number_files"],
            status=result["status"],
        )
        return group
