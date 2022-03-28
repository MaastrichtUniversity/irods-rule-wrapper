from irodsrulewrapper.decorator import rule_call
from irodsrulewrapper.dto.drop_zones import DropZones, DropZone
from irodsrulewrapper.dto.metadata_json import MetadataJSON
from irodsrulewrapper.dto.metadata_pid import MetadataPID
from irodsrulewrapper.dto.metadata_xml import MetadataXML
from irodsrulewrapper.dto.token import Token
from irodsrulewrapper.utils import (
    BaseRuleManager,
    RuleInfo,
    RuleInputValidationError,
    check_collection_id_format,
    check_project_id_format,
    log_warning_message,
)


class IngestRuleManager(BaseRuleManager):
    def __init__(self, client_user=None, admin_mode=False):
        BaseRuleManager.__init__(self, client_user, admin_mode=admin_mode)

    @rule_call
    def get_active_drop_zones(self, report):
        """
        Get the list of active drop zones

        Parameters
        ----------
        report : str
            'true'/'false' excepted values; If true, show extra values: startDate, endDate & userName

        Returns
        -------
        DropZones
            dto.DropZones object
        """
        if report != "false" and report != "true":
            raise RuleInputValidationError("invalid value for *report: expected 'true' or 'false'")

        return RuleInfo(name="listActiveDropZones", get_result=True, session=self.session, dto=DropZones)

    @rule_call
    def get_active_drop_zone(self, token, check_ingest_resource_status, dropzone_type):
        """
        Get the list of active drop zones

        Parameters
        ----------
        token : str
            The dropzone token
        check_ingest_resource_status : str
            'true'/'false' excepted values; If true, show the project resource status
        dropzone_type : str
            The type of dropzone, 'mounted' or 'direct'

        Returns
        -------
        DropZone
            dto.DropZone object
        """
        if not isinstance(token, str):
            raise RuleInputValidationError("invalid type for *token: expected a string")
        if check_ingest_resource_status not in ("false", "true"):
            raise RuleInputValidationError(
                "invalid value for *check_ingest_resource_status: expected 'true' or 'false'"
            )
        if dropzone_type not in ("mounted", "direct"):
            raise RuleInputValidationError("invalid value for *dropzone_type: expected 'mounted' or 'direct'")
        return RuleInfo(name="get_active_drop_zone", get_result=True, session=self.session, dto=DropZone)

    @rule_call
    def start_ingest(self, user, token, dropzone_type):
        """
        Start an ingest

        Parameters
        ----------
        user : str
            The user making the ingestion request
        token : str
            The dropzone token
        dropzone_type: str
            The type of dropzone (mounted or direct)
        """
        if not isinstance(user, str):
            raise RuleInputValidationError("invalid type for *user: expected a string")
        if not isinstance(token, str):
            raise RuleInputValidationError("invalid type for *token: expected a string")
        if dropzone_type not in ("mounted", "direct"):
            raise RuleInputValidationError("invalid value for *dropzone_type: expected 'mounted' or 'direct'")
        return RuleInfo(name="start_ingest", get_result=False, session=self.session, dto=None)

    def ingest(self, user, token, dropzone_type):
        """
        Ingest the requested dropzone
        NOTE: We do the 'set_total_size_dropzone' here. This allows for the progress bar to be visible in the frontend.
        However, this call can fail and the ingestion will still continue. This is by design, because we do not know
        the duration the call will take for huge dropzones.

        Parameters
        ----------
        user: str
            The user requesting the ingest
        token: str
            The dropzone token to be ingested
        dropzone_type : str
            The type of dropzone, 'mounted' or 'direct'
        """
        try:
            self.set_total_size_dropzone(token, dropzone_type)
        except Exception as e:
            log_warning_message(user, f"set_total_size_dropzone failed with error: {e}")
        if dropzone_type == "direct":
            self.set_acl("default", "own", user, f"/nlmumc/ingest/direct/{token}/instance.json")
            self.set_acl("default", "own", user, f"/nlmumc/ingest/direct/{token}/schema.json")
        self.start_ingest(user, token, dropzone_type)

    def read_metadata_xml_from_dropzone(self, token):
        xml_path = "/nlmumc/ingest/zones/" + token + "/" + "metadata.xml"
        return MetadataXML.read_metadata_xml(self.session, xml_path, token)

    def create_drop_zone(self, data: dict, schema_path: str, instance: dict, schema_name: str, schema_version: str):
        """
        Calls the createIngest rule and then save the schema.json & instance.json to the newly created drop-zone.

        Parameters
        ----------
        data: dict
            The input parameters for the createIngest rule
        schema_path: str
            The full path of the metadata schema
        instance: dict
            The instance.json as a dict
        schema_name: str
            The filename of the schema used for this dropzone (without the extension)
        schema_version: str
           The version of the schema used for this dropzone

        Returns
        -------
        str
            The drop-zone token
        """
        token = self.__create_dropzone(
            data["dropzone_type"], data["user"], data["project"], data["title"], schema_name, schema_version
        ).token
        data["token"] = token
        self.write_dropzone_metadata_files(data["dropzone_type"], token, schema_path, instance)
        return token

    @rule_call
    def __create_dropzone(self, dropzone_type, username, project_id, title, schema_name, schema_version):
        return RuleInfo(name="create_drop_zone", get_result=True, session=self.session, dto=Token)

    def write_dropzone_metadata_files(self, dropzone_type: str, token: str, schema_path: str, instance: dict):
        """
        Save the schema.json & instance.json to the indicated drop-zone.

        Parameters
        ----------
        dropzone_type: str
            The type of dropzone that was created
        token: str
            The drop-zone token
        schema_path: str
            The full path of the metadata schema
        instance: dict
            The instance.json as a dict
        """
        metadata_json = MetadataJSON(self.session)
        dropzone_path = f"/nlmumc/ingest/{'direct' if dropzone_type == 'direct' else 'zones'}/{token}"
        schema_irods_path = f"{dropzone_path}/schema.json"
        metadata_json.write_schema(schema_path, schema_irods_path)
        instance_irods_path = f"{dropzone_path}/instance.json"
        metadata_json.write_instance(instance, instance_irods_path)

    def write_instance_to_dropzone(self, instance: dict, token, dropzone_type):
        """
        Save the instance.json to the indicated iRODS path.

        Parameters
        ----------
        instance: dict
            The instance.json as a dict
        token : str
            The dropzone token
        dropzone_type: str
            The type of dropzone (mounted or direct)
        """
        metadata_json = MetadataJSON(self.session)
        dropzone_path = f"/nlmumc/ingest/{'direct' if dropzone_type == 'direct' else 'zones'}/{token}"
        instance_irods_path = dropzone_path + "/instance.json"
        if dropzone_type == "direct":
            self.set_acl("default", "write", self.session.username, instance_irods_path)
        metadata_json.write_instance(instance, instance_irods_path)
        if dropzone_type == "direct":
            self.set_acl("default", "read", self.session.username, instance_irods_path)

    def read_schema_from_dropzone(self, token, dropzone_type):
        metadata_json = MetadataJSON(self.session)
        dropzone_path = f"/nlmumc/ingest/{'direct' if dropzone_type == 'direct' else 'zones'}/{token}"
        schema_irods_path = dropzone_path + "/schema.json"
        schema = metadata_json.read_irods_json_file(schema_irods_path)

        return schema

    def read_instance_from_dropzone(self, token, dropzone_type):
        metadata_json = MetadataJSON(self.session)
        dropzone_path = f"/nlmumc/ingest/{'direct' if dropzone_type == 'direct' else 'zones'}/{token}"
        instance_irods_path = dropzone_path + "/instance.json"
        instance = metadata_json.read_irods_json_file(instance_irods_path)

        return instance

    @rule_call
    def edit_drop_zone(self, token, project, title, dropzone_type):
        """
        Edits the dropzone's project and title AVUs

        Parameters
        ----------
        token : str
            the token of the DZ to modify
        project : str
            the new project number (ex. P000000001)
        title : str
            the new title (ex. bar)
        dropzone_type: str
            The type of dropzone (mounted or direct)
        """

        dropzone_path = f"/nlmumc/ingest/{'direct' if dropzone_type == 'direct' else 'zones'}/{token}"
        input_params = {
            "*dropzonePath": '"{}"'.format(dropzone_path),
            "*project": '"{}"'.format(project),
            "*title": '"{}"'.format(title),
        }

        rule_body = """
               execute_rule{
                   editIngest;
               }
               """

        return RuleInfo(
            name="editIngest",
            get_result=False,
            session=self.session,
            dto=None,
            input_params=input_params,
            rule_body=rule_body,
        )

    @rule_call
    def generate_token(self):
        """
        Gets a unused (dropzone) token generated by iRODS

        Returns
        -------
        Token
            The token generated by iRODS

        """

        return RuleInfo(name="generate_token", get_result=True, session=self.session, dto=Token)

    @rule_call
    def set_total_size_dropzone(self, token, dropzone_type):
        """
        Set an attribute value to the input user

        Parameters
        ----------
        token : str
            The dropzone token to be ingested
        dropzone_type: str
            The type of dropzone, 'mounted' or 'direct'

        """
        if type(token) != str:
            raise RuleInputValidationError("invalid type for *token: expected a string")
        if dropzone_type not in ("mounted", "direct"):
            raise RuleInputValidationError("invalid value for *dropzone_type: expected 'mounted' or 'direct'")

        return RuleInfo(name="set_dropzone_total_size_avu", get_result=False, session=self.session, dto=None)

    @rule_call
    def get_versioned_pids(self, project_id, collection_id, version):
        """
        Request a PID via epicpid

        Parameters
        ----------
        project_id : str
            The project to request and set a pid for (ie. P000000010)
        collection_id : str
            The collection to request and set a PID for (ie. C000000002)
        version : str
            The version number of collection,schema and instance that PID are requested for
        """
        if not check_project_id_format(project_id):
            raise RuleInputValidationError("invalid project's path format: e.g P000000010")
        if not check_collection_id_format(collection_id):
            raise RuleInputValidationError("invalid collection id; eg. C000000001")

        return RuleInfo(name="get_versioned_pids", get_result=True, session=self.session, dto=MetadataPID)

    @rule_call
    def create_ingest_metadata_snapshot(self, project_id, collection_id, source_collection, overwrite_flag):
        """
        Create a snapshot of the collection metadata files (schema & instance):
            * Check if the snapshot folder (.metadata_versions) already exists, if not create it
            * Copy the current metadata files to .metadata_versions and add a version 1 in the filename

        Parameters
        ----------
        project_id : str
            The project where the instance.json is to fill (e.g: P000000010)
        collection_id : str
            The collection where the instance.json is to fill (e.g: C000000002)
        source_collection: str
            The drop-zone absolute path (e.g: /nlmumc/ingest/zones/crazy-frog)
        overwrite_flag: str
            'true'/'false' expected; If true, the copy overwrites possible existing schema.1.json & instance.1.json files
        """
        if not check_project_id_format(project_id):
            raise RuleInputValidationError("invalid project's path format: e.g P000000010")
        if not check_collection_id_format(collection_id):
            raise RuleInputValidationError("invalid collection id; eg. C000000001")
        if not isinstance(source_collection, str):
            raise RuleInputValidationError("invalid type for *source_collection: expected a string")
        if overwrite_flag != "false" and overwrite_flag != "true":
            raise RuleInputValidationError("invalid value for *overwrite_flag: expected 'true' or 'false'")

        return RuleInfo(name="create_ingest_metadata_snapshot", get_result=False, session=self.session, dto=None)
