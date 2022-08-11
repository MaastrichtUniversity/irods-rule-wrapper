"""This module contains the MetadataJSON helper class."""
import errno
import time
import os
import json

from irods import exception
from irods.session import iRODSSession

from irodsrulewrapper.utils import log_error_message


class MetadataJSON:
    """This class has the helper functions to write/read metadata json files from iRODS."""

    def __init__(self, session: iRODSSession):
        self.session = session

    def write_schema(self, schema_path: str, schema_irods_path: str):
        """
        Put the schema.json from the schema_path inside the drop-zone

        Parameters
        ----------
        schema_path: str
            The full path of the metadata schema
        schema_irods_path: str
            The iRODS full path of the metadata schema
        """
        self.session.data_objects.put(schema_path, schema_irods_path)

    def write_instance(self, instance: dict, instance_irods_path: str):
        """
        Put the instance.json from the schema_path inside the drop-zone.
        data_objects.put seems to required that the input file is physically on disk.
        So we create a temporary instance on disk and delete it at the end of the method.

        Parameters
        ----------
        instance: dict
            The instance.json as a dict
        instance_irods_path: str
            The iRODS full path of the metadata instance
        """
        timestamp = time.time_ns()
        # create a temporary file with the epoch timestamp in the filename to avoid collision
        instance_path = f"./instance_{timestamp}.json"
        with open(instance_path, "w", encoding="utf-8") as instance_file:
            json.dump(instance, instance_file, ensure_ascii=False, indent=4)
        self.session.data_objects.put(instance_path, instance_irods_path)
        os.remove(instance_path)

    def read_irods_json_file(self, irods_file_path) -> dict:
        """
        Open the json file at the iRODS path and parse it JSON.

        Parameters
        ----------
        irods_file_path: str
            The iRODS full path of the metadata file

        Returns
        -------
        dict
            The json schema
        """
        try:
            with self.session.data_objects.open(irods_file_path, "r") as irods_file:
                json_string = irods_file.read()
        except (exception.DataObjectDoesNotExist, exception.SYS_FILE_DESC_OUT_OF_RANGE):
            log_error_message(self.session.username, f"{irods_file_path} is missing")
        else:
            return json.loads(json_string)
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), irods_file_path)
