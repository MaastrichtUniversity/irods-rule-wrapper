"""This module contains the CollectionRuleManager class."""
import json

from cedarparsingutils.dto.general_instance import GeneralInstance
from dhpythonirodsutils import validators, exceptions, formatters

from irodsrulewrapper.decorator import rule_call
from irodsrulewrapper.dto.attribute_value import AttributeValue
from irodsrulewrapper.dto.boolean import Boolean
from irodsrulewrapper.dto.collection_details import CollectionDetails
from irodsrulewrapper.dto.collections import Collection
from irodsrulewrapper.dto.collections import Collections
from irodsrulewrapper.dto.metadata_json import MetadataJSON
from irodsrulewrapper.utils import BaseRuleManager, RuleInfo, RuleInputValidationError


class CollectionRuleManager(BaseRuleManager):
    """This class bundles the collection related wrapped rules and helper methods."""

    def __init__(self, client_user=None, admin_mode=False):
        BaseRuleManager.__init__(self, client_user, admin_mode=admin_mode)

    @rule_call
    def open_project_collection(self, project, project_collection, user, rights):
        """
        Set the ACL of a given collection

        Parameters
        ----------
        project : str
            Project id
        project_collection : str
            Collection id
        user : str
            The username
        rights : str
            access level: 'own', 'write', 'read'
        """
        try:
            validators.validate_project_id(project)
            validators.validate_collection_id(project_collection)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("invalid project or collection id; eg. P000000001") from err

        if not isinstance(user, str):
            raise RuleInputValidationError("invalid type for *user: expected a string")

        if not isinstance(rights, str):
            raise RuleInputValidationError("invalid type for *rights: expected a string")

        return RuleInfo(name="openProjectCollection", get_result=False, session=self.session, dto=None)

    @rule_call
    def close_project_collection(self, project, project_collection):
        """
        Set the ACL of a given collection

        Parameters
        ----------
        project : str
            Project id
        project_collection : str
            Collection id
        """
        try:
            validators.validate_project_id(project)
            validators.validate_collection_id(project_collection)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("invalid project or collection id; eg. P000000001") from err

        return RuleInfo(name="close_project_collection", get_result=False, session=self.session, dto=None)

    @rule_call
    def set_collection_avu(self, collection_path, attribute, value):
        """
        Set a collection AVU

        Parameters
        ----------
        collection_path : str
            The collection's absolute path; eg. /nlmumc/projects/P000000001/C000000001
        attribute: str
            The attribute that is going to be set; e.g 'responsibleCostCenter'
        value: str
            The value that is going to bet set; e.g 'UM-12345678N'
        """
        try:
            validators.validate_irods_collection(collection_path)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("invalid path format") from err

        if not isinstance(attribute, str):
            raise RuleInputValidationError("invalid type for *attribute: expected a string")

        if not isinstance(value, str):
            raise RuleInputValidationError("invalid type for *value: expected a string")

        return RuleInfo(name="setCollectionAVU", get_result=False, session=self.session, dto=None)

    @rule_call
    def get_collections(self, project_path):
        """
        Get the list of project's collections

        Parameters
        ----------
        project_path : str
            The project's absolute path; eg. /nlmumc/projects/P000000010

        Returns
        -------
        Collections
            dto.Collections object
        """
        if not validators.validate_project_path(project_path):
            raise RuleInputValidationError("invalid project's path format: eg. /nlmumc/projects/P000000010")

        return RuleInfo(
            name="list_collections",
            get_result=True,
            session=self.session,
            dto=Collections,
            parse_to_dto=self.parse_to_dto,
        )

    @rule_call
    def get_project_collection_details(self, project, collection, inherited):
        """
        Lists the destination resources and their statuses

        Parameters
        ----------
        project : str
            The collection's absolute path; eg. P000000001
        collection : str
            The collection's id; eg. C000000001
        inherited: str
            The attribute that is going to be set; e.g 'responsibleCostCenter'

        Returns
        -------
        Collection
            The collection avu & acl

        """
        try:
            validators.validate_project_id(project)
            validators.validate_collection_id(collection)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("invalid project or collection id; eg. P000000001") from err

        try:
            validators.validate_string_boolean(inherited)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("invalid value for *inherited: expected 'true' or 'false'") from err

        return RuleInfo(name="detailsProjectCollection", get_result=True, session=self.session, dto=CollectionDetails)

    @rule_call
    def archive_project_collection(self, collection: str, initiator: str):
        """
        Archive all the eligible files from the collection to tape

        Parameters
        ----------
        collection: str
            The absolute collection path: e.g /nlmumc/projects/P000000010/C000000001
        initiator: str
            The user who started the process
        """
        try:
            validators.validate_project_collection_path(collection)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("invalid collection id; eg. C000000001") from err

        if not isinstance(initiator, str):
            raise RuleInputValidationError("invalid type for *initiator: expected a string")

        return RuleInfo(name="start_archive", get_result=False, session=self.session, dto=None)

    @rule_call
    def unarchive_project_collection(self, path: str, initiator: str):
        """
        Un-archive a single file or entire collection from tape

        Parameters
        ----------
        path: str
            The absolute path of the collection or the single file to un-archive
            e.g: /nlmumc/projects/P000000010/C000000001 or /nlmumc/projects/P000000010/C000000001/test.txt
        initiator: str
            The user who started the process
        """
        if not isinstance(path, str):
            raise RuleInputValidationError("invalid type for *path: expected a string")

        if not isinstance(initiator, str):
            raise RuleInputValidationError("invalid type for *initiator: expected a string")

        return RuleInfo(name="start_unarchive", get_result=False, session=self.session, dto=None)

    @rule_call
    def get_collection_attribute_value(self, path, attribute):
        """
        Get the attribute value of an iRODS collection

        Parameters
        ----------
        path: str
            The absolute path of the collection
            e.g: /nlmumc/projects/P000000010/C000000001 or /nlmumc/ingest/zones/grieving-giant
        attribute: str
            The attribute to query

        Returns
        -------
        AttributeValue
            dto.AttributeValue object
        """

        if not isinstance(path, str):
            raise RuleInputValidationError("invalid type for *path: expected a string")

        if not isinstance(attribute, str):
            raise RuleInputValidationError("invalid type for *attribute: expected a string")

        return RuleInfo(
            name="get_collection_attribute_value", get_result=True, session=self.session, dto=AttributeValue
        )

    def read_schema_from_collection(self, project_id: str, collection_id: str) -> dict:
        """
        Returns the object version of the schema.json on the collections root

        Parameters
        ----------
        project_id: str
            The project ID ie P000000001
        collection_id: str
            The collection ID ie C000000001

        Returns
        -------
        dict
            The schema json
        """
        metadata_json = MetadataJSON(self.session)
        schema_irods_path = formatters.format_schema_collection_path(project_id, collection_id)
        try:
            validators.validate_file_path(schema_irods_path)
            validators.validate_full_path_safety(schema_irods_path)
            return metadata_json.read_irods_json_file(schema_irods_path)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("invalid schema path provided") from err

    def read_schema_version_from_collection(self, project_id: str, collection_id: str, version: str) -> dict:
        """
        Returns the version stamped object version of the schema.json in the '.metadata_versions/' directory

        Parameters
        ----------
        project_id: str
            The project ID ie P000000001
        collection_id: str
            The collection ID ie C000000001
        version: str
            The verion of the schema to retrieve

        Returns
        -------
        dict
            The schema json
        """
        metadata_json = MetadataJSON(self.session)
        schema_irods_path = formatters.format_schema_versioned_collection_path(project_id, collection_id, version)
        try:
            validators.validate_file_path(schema_irods_path)
            validators.validate_full_path_safety(schema_irods_path)
            return metadata_json.read_irods_json_file(schema_irods_path)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("invalid schema path provided") from err

    def read_instance_from_collection(self, project_id: str, collection_id: str) -> dict:
        """
        Returns the object version of the instance.json on the collections root

        Parameters
        ----------
        project_id: str
            The project ID ie P000000001
        collection_id: str
            The collection ID ie C000000001

        Returns
        -------
        dict
            The instance json
        """
        metadata_json = MetadataJSON(self.session)
        instance_irods_path = formatters.format_instance_collection_path(project_id, collection_id)
        try:
            validators.validate_file_path(instance_irods_path)
            validators.validate_full_path_safety(instance_irods_path)
            return metadata_json.read_irods_json_file(instance_irods_path)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("invalid instance path provided") from err

    @staticmethod
    def parse_general_instance(instance: dict) -> GeneralInstance:
        """
        Parse an instance.json as dict to a GeneralInstance DTO.

        Parameters
        ----------
        instance: dict
            The instance.json as dict to parse

        Returns
        -------
        GeneralInstance
            The parsed instance as a GeneralInstance DTO
        """
        return GeneralInstance.create_from_dict(instance)

    def read_instance_version_from_collection(self, project_id: str, collection_id: str, version: str) -> dict:
        """
        Returns the version stamped object version of the instance.json in the '.metadata_versions/' directory

        Parameters
        ----------
        project_id: str
            The project ID ie P000000001
        collection_id: str
            The collection ID ie C000000001
        version: str
            The verion of the instance to retrieve

        Returns
        -------
        dict
            The instance json
        """
        metadata_json = MetadataJSON(self.session)
        instance_irods_path = formatters.format_instance_versioned_collection_path(project_id, collection_id, version)
        try:
            validators.validate_file_path(instance_irods_path)
            validators.validate_full_path_safety(instance_irods_path)
            return metadata_json.read_irods_json_file(instance_irods_path)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("invalid instance path provided") from err  # Raise different error

    @rule_call
    def set_collection_size(self, project_id, collection_id, open_collection, close_collection):
        """
        Recalculates the collection size and number of files.

        Parameters
        ----------
        project_id: str
            The project ID ie P000000001
        collection_id: str
            The collection ID ie C000000001
        open_collection: str
            'true'/'false' expected; If true, open the collection ACL for the current user
        close_collection: str
            'true'/'false' expected; If true, close the collection ACL.
        """
        try:
            validators.validate_project_id(project_id)
            validators.validate_collection_id(collection_id)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("invalid project or collection id; eg. P000000001") from err

        expected_values = ["false", "true"]
        if open_collection not in expected_values and close_collection not in expected_values:
            raise RuleInputValidationError(
                "invalid value for *open_collection/close_collection: expected 'true' or 'false'"
            )
        return RuleInfo(name="setCollectionSize", get_result=False, session=self.session, dto=None)

    @rule_call
    def get_collection_tree(self, relative_path):
        """
        Lists the folders and files attributes at the input 'path'

        Parameters
        ----------
        relative_path : str
           Relative path to collection; e.g: P000000014/C000000001/.metadata_versions

        Returns
        -------
        dict
           The folders and files attributes at the requested path
        """
        return RuleInfo(
            name="get_collection_tree", get_result=True, session=self.session, dto=None, parse_to_dto=self.parse_to_dto
        )

    @rule_call
    def create_collection_metadata_snapshot(self, project_id, collection_id):
        """
        Create a snapshot of the collection metadata files (schema & instance):
            * Check user edit metadata permission
            * Check if the snapshot folder (.metadata_versions) already exists, if not create it
            * Request the new versions handle PIDs
            * Update instance.json and schema.json properties
            * Copy the current metadata files to .metadata_versions and add the version number in the filename
            * Increment the AVU latest_version_number

        Parameters
        ----------
        project_id : str
            The project where the instance.json is to fill (e.g: P000000010)
        collection_id : str
            The collection where the instance.json is to fill (e.g: C000000002)

        Returns
        -------
        bool
            PIDs request status; If true, the handle PIDs were successfully requested.
        """
        try:
            validators.validate_project_id(project_id)
            validators.validate_collection_id(collection_id)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("invalid project or collection id; eg. P000000001") from err

        return RuleInfo(name="create_collection_metadata_snapshot", get_result=True, session=self.session, dto=Boolean)

    def save_metadata_json_to_collection(self, project_id, collection_id, instance, schema_dict):
        """
        After a user edits the collection metadata, this method takes care of metadata saving workflow:
            * Check if the AVU latest_version_number exists and is an integer
            * Overwrite the current instance with the new one
            * Check if we need to overwrite the schema, if yes do it
            * Create a snapshot of the new collection metadata
            * Update collection-AVUs: 'schemaVersion', 'schemaName' & 'title'
            * Run the rule that recalculates the collection size and number of files

        Parameters
        ----------
        project_id: str
            The project ID ie P000000001
        collection_id: str
            The collection ID ie C000000001
        schema_dict: dict
            Contains the following key-value pairs: overwrite, title, schema_path, schema_version, schema_file_name
        instance: dict
            The json formatted instance data

        Returns
        -------
        bool
            PIDs request status; If true, the handle PIDs were successfully requested.
        """
        try:
            validators.validate_project_id(project_id)
            validators.validate_collection_id(collection_id)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("invalid project id; eg. P000000001") from err

        collection_path = formatters.format_project_collection_path(project_id, collection_id)
        schema_irods_path = formatters.format_schema_collection_path(project_id, collection_id)
        instance_irods_path = formatters.format_instance_collection_path(project_id, collection_id)

        latest_version_number = self.get_collection_attribute_value(collection_path, "latest_version_number").value
        if not latest_version_number.isdigit():
            raise RuleInputValidationError(
                f"The AVU 'latest_version_number' for {collection_path} is incorrect: {latest_version_number}"
            )

        metadata_json = MetadataJSON(self.session)
        metadata_json.write_instance(instance, instance_irods_path)
        if schema_dict["overwrite"]:
            metadata_json.write_schema(schema_dict["schema_path"], schema_irods_path)

        self.set_collection_avu(collection_path, "schemaVersion", schema_dict["schema_version"])
        self.set_collection_avu(collection_path, "schemaName", schema_dict["schema_file_name"])
        self.set_collection_avu(collection_path, "title", schema_dict["title"])
        pid_request_status = self.create_collection_metadata_snapshot(project_id, collection_id)

        return pid_request_status

    @rule_call
    def set_acl_for_metadata_snapshot(
        self, project_id: str, collection_id: str, user: str, open_acl: str, close_acl: str
    ):
        """
        Modify the ACL of the given project collection for the given user to be able to create the metadata snapshot.

        Parameters
        ----------
        project_id: str
            The project ID ie P000000001
        collection_id: str
            The collection ID ie C000000001
        user: str
            The username
        open_acl: str
            'true'/'false' expected; If true, open the collection ACL for the current user
        close_acl: str
            'true'/'false' expected; If true, open the collection ACL for the current user
        """
        try:
            validators.validate_project_id(project_id)
            validators.validate_collection_id(collection_id)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("invalid project or collection id; eg. P000000001") from err

        if not isinstance(user, str):
            raise RuleInputValidationError("invalid type for *user: expected a string")

        expected_values = ["false", "true"]
        if open_acl not in expected_values and close_acl not in expected_values:
            raise RuleInputValidationError("invalid value for *open_acl/close_acl: expected 'true' or 'false'")

        return RuleInfo(name="set_acl_for_metadata_snapshot", get_result=False, session=self.session, dto=None)

    @rule_call
    def revoke_project_collection_user_access(self, user_project_collection: str, reason: str, description: str):
        """
        Revoke all user access to the input project collection, after a deletion have been requested.

        Parameters
        ----------
        user_project_collection : str
            The absolute path of the project collection
        reason : str
            The reason of the deletion
        description : str
            An optional description providing additional details, empty string if not provided by the form/user
        """
        try:
            validators.validate_project_collection_path(user_project_collection)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError(
                "invalid project collection path; eg. /nlmumc/projects/P000000010/C000000070"
            ) from err

        if not isinstance(reason, str):
            raise RuleInputValidationError("invalid type for *reason: expected a string")

        if not isinstance(description, str):
            raise RuleInputValidationError("invalid type for *description: expected a string")

        return RuleInfo(name="revoke_project_collection_user_access", get_result=False, session=self.session, dto=None)

    @rule_call
    def get_project_collection_process_activity(self, user_project_collection: str):
        """
        Query for any process activity linked to the input project collection.

        Parameters
        ----------
        user_project_collection : str
            The absolute path of the project collection

        Returns
        -------
        Boolean
            True, if the project collection has at least one active process.
        """
        try:
            validators.validate_project_collection_path(user_project_collection)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError(
                "invalid project collection path; eg. /nlmumc/projects/P000000010/C000000070"
            ) from err

        return RuleInfo(
            name="get_project_collection_process_activity", get_result=True, session=self.session, dto=Boolean
        )
