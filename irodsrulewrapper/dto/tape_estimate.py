from typing import Dict


class TapeEstimate:
    def __init__(self, above_threshold_bytes_size: str, above_threshold_number_files: str,
                 archivable_bytes_size: str, archivable_number_files: str, status: str):
        self.above_threshold_bytes_size: str = above_threshold_bytes_size
        self.above_threshold_number_files: str = above_threshold_number_files
        self.archivable_bytes_size: str = archivable_bytes_size
        self.archivable_number_files: str = archivable_number_files
        self.status: str = status

    @classmethod
    def create_from_rule_result(cls, result: Dict) -> 'TapeEstimate':

        group = cls(result["above_threshold"]["bytes_size"], result["above_threshold"]["number_files"],
                    result["archivable"]["bytes_size"], result["archivable"]["number_files"],
                    result["status"])
        return group
