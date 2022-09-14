"""This module contains the IngestRuleManager class."""
from dhpythonirodsutils import validators, formatters, exceptions

from irodsrulewrapper.decorator import rule_call
from irodsrulewrapper.dto.drop_zones import DropZones, DropZone
from irodsrulewrapper.dto.metadata_json import MetadataJSON
from irodsrulewrapper.dto.metadata_pid import MetadataPID
from irodsrulewrapper.dto.token import Token
from irodsrulewrapper.rule_managers.projects import ProjectRuleManager
from irodsrulewrapper.utils import (
    BaseRuleManager,
    RuleInfo,
    RuleInputValidationError,
    log_warning_message,
)


class IngestRuleManager(BaseRuleManager):
    """This class bundles the dropzone and ingestion related wrapped rules and helper methods."""

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
        try:
            validators.validate_string_boolean(report)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("invalid value for *report: expected 'true' or 'false'") from err

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
        try:
            validators.validate_string_boolean(check_ingest_resource_status)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError(
                "invalid value for *check_ingest_resource_status: expected 'true' or 'false'"
            ) from err
        try:
            validators.validate_dropzone_type(dropzone_type)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("invalid value for *dropzone_type: expected 'mounted' or 'direct'") from err
        return RuleInfo(name="get_active_drop_zone", get_result=True, session=self.session, dto=DropZone)

    @rule_call
    def start_ingest(self, user, token, dropzone_type):
        """
        Start the ingestion workflow.

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
        try:
            validators.validate_dropzone_type(dropzone_type)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("invalid value for *dropzone_type: expected 'mounted' or 'direct'") from err
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
        except RuntimeError as err:
            log_warning_message(user, f"set_total_size_dropzone failed with error: {err}")
        if dropzone_type == "direct":
            # CAUTION: This is an admin level rule call
            admin_rule_manager = ProjectRuleManager(admin_mode=True)
            admin_rule_manager.set_acl(
                "default", "admin:own", user, formatters.format_instance_dropzone_path(token, dropzone_type)
            )
            admin_rule_manager.set_acl(
                "default", "admin:own", user, formatters.format_schema_dropzone_path(token, dropzone_type)
            )
        self.start_ingest(user, token, dropzone_type)

    def create_drop_zone(self, data: dict, schema_path: str, instance: dict, schema_name: str, schema_version: str):
        """
        Calls:
            * the createIngest rule.
            * save the schema.json & instance.json to the newly created drop-zone.
            * transfer the project ACL to the newly created drop-zone.

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
        self.write_dropzone_metadata_files(data["dropzone_type"], token, schema_path, instance)
        if data["dropzone_type"] == "direct":
            self.set_project_acl_to_dropzone(data["project"], token, "true")

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
        metadata_json.write_schema(schema_path, formatters.format_schema_dropzone_path(token, dropzone_type))
        metadata_json.write_instance(instance, formatters.format_instance_dropzone_path(token, dropzone_type))

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
        instance_irods_path = formatters.format_instance_dropzone_path(token, dropzone_type)

        prefix = ""
        # If the user calling this rule is 'rods' we need to escalate
        if self.session.username == "rods":
            prefix = "admin:"

        if dropzone_type == "direct":
            self.set_acl("default", f"{prefix}write", self.session.username, instance_irods_path)
        metadata_json.write_instance(instance, instance_irods_path)
        if dropzone_type == "direct":
            self.set_acl("default", f"{prefix}read", self.session.username, instance_irods_path)

    def read_schema_from_dropzone(self, token, dropzone_type) -> dict:
        """
        Save the schema.json to the indicated iRODS path.

        Parameters
        ----------
        token : str
            The dropzone token
        dropzone_type: str
            The type of dropzone (mounted or direct)

        Returns
        -------
        dict
            The json schema
        """
        metadata_json = MetadataJSON(self.session)
        schema = metadata_json.read_irods_json_file(formatters.format_schema_dropzone_path(token, dropzone_type))

        return schema

    def read_instance_from_dropzone(self, token, dropzone_type) -> dict:
        """
        Read the instance.json from the indicated iRODS path.

        Parameters
        ----------
        token : str
            The dropzone token
        dropzone_type: str
            The type of dropzone (mounted or direct)

        Returns
        -------
        dict
            The json instance.
        """
        metadata_json = MetadataJSON(self.session)
        instance = metadata_json.read_irods_json_file(formatters.format_instance_dropzone_path(token, dropzone_type))

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

        input_params = {
            "*dropzonePath": f'"{formatters.format_dropzone_path(token, dropzone_type)}"',
            "*project": f'"{project}"',
            "*title": f'"{title}"',
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
        Gets an unused (dropzone) token generated by iRODS

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
        if not isinstance(token, str):
            raise RuleInputValidationError("invalid type for *token: expected a string")
        try:
            validators.validate_dropzone_type(dropzone_type)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("invalid value for *dropzone_type: expected 'mounted' or 'direct'") from err

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
        try:
            validators.validate_project_id(project_id)
            validators.validate_collection_id(collection_id)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("invalid project or collection id format: e.g P000000010") from err

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
            'true'/'false' expected; If true, the copy overwrites possible existing schema.1.json
            & instance.1.json files
        """
        try:
            validators.validate_project_id(project_id)
            validators.validate_collection_id(collection_id)
            validators.validate_string_boolean(overwrite_flag)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("invalid project id, collection id or overwrite flag") from err

        if not isinstance(source_collection, str):
            raise RuleInputValidationError("invalid type for *source_collection: expected a string")

        return RuleInfo(name="create_ingest_metadata_snapshot", get_result=False, session=self.session, dto=None)

    @rule_call
    def get_dropzone_folders(self, token, path):
        """
        Lists recursively the folders at the input 'path'

        Parameters
        ----------
        token: str
           The dropzone token
        path: str
           Relative path in dropzone for folder

        Returns
        -------
        list
           The recursive folders list at the requested path
        """
        try:
            validators.validate_dropzone_token(token)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("invalid dropzone token: e.g crazy-frog") from err
        if not isinstance(path, str):
            raise RuleInputValidationError("invalid type for *path: expected a string")
        return RuleInfo(
            name="get_dropzone_folders", get_result=True, session=self.session, dto=None, parse_to_dto=self.parse_to_dto
        )

    @rule_call
    def get_dropzone_files(self, token, directory):
        """
        Lists the folders and files attributes at the input 'directory'

        Parameters
        ----------
        token : str
           The dropzone token
        directory: str
            The directory to list the folders and files of

        Returns
        -------
        list
           The folders and files attributes at the requested path
        """
        try:
            validators.validate_dropzone_token(token)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("invalid dropzone token: e.g crazy-frog") from err
        if not isinstance(directory, str):
            raise RuleInputValidationError("invalid type for *path: expected a string")
        return RuleInfo(
            name="get_dropzone_files", get_result=True, session=self.session, dto=None, parse_to_dto=self.parse_to_dto
        )

    @rule_call
    def set_project_acl_to_dropzones(self, project_id):
        """
        This rule transfers the ACLs that exist on a project level to all of its dropzones
            * Get the 'enableDropzoneSharing' avu on the project
            * Get all dropzones for the project
            * For each dropzone, depending on the enableDropzoneSharing avu perform the following:
                    * False -> Remove all contributors and managers from the dropzones except for the creator
                    * True  -> Add all contributors and managers to a dropzone with 'own' rights
        Parameters
        ----------
        project_id : str
            The project to transfer (e.g: P000000010)
        """
        try:
            validators.validate_project_id(project_id)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("invalid project or collection id: e.g P000000010") from err

        return RuleInfo(name="set_project_acl_to_dropzones", get_result=False, session=self.session, dto=None)

    @rule_call
    def set_project_acl_to_dropzone(self, project_id, dropzone_token, new_dropzone):
        """
        This rule transfers the ACLs that exist on the input project level to the input dropzone.
                * Get the 'enableDropzoneSharing' avu on the project
                * Depending on the enableDropzoneSharing avu perform the following:
                        * False -> Remove all contributors and managers from the dropzone except for the creator
                        * True  -> Add all contributors and managers to a dropzone with 'own' rights
        Parameters
        ----------
        project_id : str
            The project to transfer (e.g: P000000010)
        dropzone_token : str
            The dropzone token to update
        new_dropzone : str
            'true'/'false' expected; If true, the input dropzone has been newly created
        """
        try:
            validators.validate_project_id(project_id)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("invalid project or collection id: e.g P000000010") from err

        try:
            validators.validate_dropzone_token(dropzone_token)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("invalid dropzone token: e.g crazy-frog") from err

        try:
            validators.validate_string_boolean(new_dropzone)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("invalid value for new_dropzone: expected 'true' or 'false'") from err

        return RuleInfo(name="set_project_acl_to_dropzone", get_result=False, session=self.session, dto=None)
