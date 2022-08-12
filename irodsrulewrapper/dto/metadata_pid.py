"""This module contains the ExternalPID class and its factory constructor."""
from irodsrulewrapper.dto.dto_base_model import DTOBaseModel


class MetadataPID(DTOBaseModel):
    """This class represents the output result of a versioned EpicPID request."""

    instance_pid: dict
    collection_pid: dict
    schema_pid: dict

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "MetadataPID":
        value = cls(instance_pid=result["instance"], collection_pid=result["collection"], schema_pid=result["schema"])
        return value
