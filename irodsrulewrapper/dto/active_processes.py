"""This module contains the ActiveProcesses DTO class and its factory constructor."""
from irodsrulewrapper.dto.active_proces import ActiveProcess
from irodsrulewrapper.dto.drop_zone import DropZone
from pydantic import BaseModel


class ActiveProcesses(BaseModel):
    """
    This class represents a list of iRODS active data transfer processes (ingest, tape archive & DataverseNL export).
    """

    completed: list[DropZone | ActiveProcess]
    error: list[DropZone | ActiveProcess]
    in_progress: list[DropZone | ActiveProcess]
    open: list[DropZone]

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "ActiveProcesses":
        completed = []
        for process in result["completed"]:
            cls.parse_active_process(process, completed)
        error = []
        for process in result["error"]:
            cls.parse_active_process(process, error)
        in_progress = []
        for process in result["in_progress"]:
            cls.parse_active_process(process, in_progress)
        open_list = []
        for process in result["open"]:
            cls.parse_active_process(process, open_list)

        output = cls(completed=completed, error=error, in_progress=in_progress, open=open_list)

        return output

    @staticmethod
    def parse_active_process(process: dict, process_state_list: list):
        if process["process_type"] == "drop_zone":
            item = DropZone.create_from_rule_result(process)
        else:
            item = ActiveProcess.create_from_rule_result(process)
        process_state_list.append(item)
