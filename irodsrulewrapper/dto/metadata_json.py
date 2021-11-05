import time
import os
import json


class MetadataJSON:
    def __init__(self, session, token: str):
        self.session = session
        self.token: str = token

    def write_schema(self, schema_path):
        """
        Put the schema.json from the schema_path inside the drop-zone

        Parameters
        ----------
        schema_path: str
            The full path of the metadata schema
        """
        ingest_zone = "/nlmumc/ingest/zones/" + self.token + "/" + "schema.json"
        self.session.data_objects.put(schema_path, ingest_zone)

    def write_instance(self, instance):
        """
        Put the instance.json from the schema_path inside the drop-zone.
        data_objects.put seems to required that the input file is physically on disk.
        So we create a temporary instance on disk and delete it at the end of the method.

        Parameters
        ----------
        instance: dict
            The instance.json as a dict
        """
        timestamp = time.time_ns()
        # create a temporary file with the epoch timestamp in the filename to avoid collision
        instance_path = f"./instance_{timestamp}.json"
        with open(instance_path, "w", encoding="utf-8") as instance_file:
            json.dump(instance, instance_file, ensure_ascii=False, indent=4)
        instance_irods_path = "/nlmumc/ingest/zones/" + self.token + "/" + "instance.json"
        self.session.data_objects.put(instance_path, instance_irods_path)
        os.remove(instance_path)
