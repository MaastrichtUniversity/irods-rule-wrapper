import json
import os

from irodsrulewrapper.decorator import rule_call
from irodsrulewrapper.dto.attribute_value import AttributeValue
from irodsrulewrapper.dto.collection_details import CollectionDetails
from irodsrulewrapper.dto.collections import Collection
from irodsrulewrapper.dto.collections import Collections
from irodsrulewrapper.dto.metadata_json import MetadataJSON
from irodsrulewrapper.dto.metadata_xml import MetadataXML
from irodsrulewrapper.dto.tape_estimate import TapeEstimate
from irodsrulewrapper.utils import (
    check_project_path_format,
    check_project_collection_path_format,
    publish_message,
    check_project_id_format,
    check_collection_id_format,
    BaseRuleManager,
    RuleInfo,
    RuleInputValidationError,
    check_file_path_format,
    is_safe_full_path,
)


class CollectionRuleManager(BaseRuleManager):
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
        # Do input validation here
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
        # Do input validation here
        return RuleInfo(name="closeProjectCollection", get_result=False, session=self.session, dto=None)

    @rule_call
    def set_collection_avu(self, collection_path, attribute, value):
        """
        Set a collection AVU

        Parameters
        ----------
        collection_path : str
            The collection's absolute path; eg. /nlmumc/projects/P000000001
        attribute: str
            The attribute that is going to be set; e.g 'responsibleCostCenter'
        value: str
            The value that is going to bet set; e.g 'UM-12345678N'
        """
        if not check_project_path_format(collection_path) and not check_project_collection_path_format(collection_path):
            raise RuleInputValidationError("invalid path format")

        if type(attribute) != str:
            raise RuleInputValidationError("invalid type for *attribute: expected a string")

        if type(value) != str:
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
        if not check_project_path_format(project_path):
            raise RuleInputValidationError("invalid project's path format: eg. /nlmumc/projects/P000000010")

        return RuleInfo(name="list_collections", get_result=True, session=self.session, dto=Collections)

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
        if not check_project_id_format(project):
            raise RuleInputValidationError("invalid project id; eg. P000000001")

        if not check_collection_id_format(collection):
            raise RuleInputValidationError("invalid collection id; eg. C000000001")

        if inherited != "false" and inherited != "true":
            raise RuleInputValidationError("invalid value for *inherited: expected 'true' or 'false'")

        return RuleInfo(name="detailsProjectCollection", get_result=True, session=self.session, dto=CollectionDetails)

    @rule_call
    def get_project_collection_tape_estimate(self, project, collection):
        """
        The project collection tape status & the number and total bytes size of files eligible for tape

        Parameters
        ----------
        project: str
            The project's id; e.g P000000010
        collection: str
            The collection's id; e.g C000000001

        Returns
        -------
        dict
            The project collection tape status, above_threshold and archivable
        """
        if not check_project_id_format(project):
            raise RuleInputValidationError("invalid project id; eg. P000000001")

        if not check_collection_id_format(collection):
            raise RuleInputValidationError("invalid collection id; eg. C000000001")

        return RuleInfo(
            name="get_project_collection_tape_estimate", get_result=True, session=self.session, dto=TapeEstimate
        )

    @rule_call
    def archive_project_collection(self, collection):
        """
        Archive all the eligible files from the collection to tape

        Parameters
        collection: str
            The absolute collection path: e.g /nlmumc/projects/P000000010/C000000001

        """
        if not check_project_collection_path_format(collection):
            raise RuleInputValidationError("invalid collection id; eg. C000000001")

        return RuleInfo(name="prepareTapeArchive", get_result=False, session=self.session, dto=None)

    @rule_call
    def unarchive_project_collection(self, path):
        """
        Un-archive a single file or entire collection from tape

        Parameters
        ----------
        path: str
            The absolute path of the collection or the single file to un-archive
            e.g: /nlmumc/projects/P000000010/C000000001 or /nlmumc/projects/P000000010/C000000001/test.txt
        """

        return RuleInfo(name="prepareTapeUnArchive", get_result=False, session=self.session, dto=None)

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

        if type(path) != str:
            raise RuleInputValidationError("invalid type for *path: expected a string")

        if type(attribute) != str:
            raise RuleInputValidationError("invalid type for *attribute: expected a string")

        return RuleInfo(
            name="get_collection_attribute_value", get_result=True, session=self.session, dto=AttributeValue
        )

    def read_metadata_xml_from_collection(self, project_id, collection_id):
        xml_path = "/nlmumc/projects/" + project_id + "/" + collection_id + "/" + "metadata.xml"
        return MetadataXML.read_metadata_xml(self.session, xml_path)

    def export_project_collection(self, project, collection, repository, message):
        """
        Starts the exporting process of a collection. Be sure to call this rule
        as 'rodsadmin' because it will open a collection using admin-mode.

        Parameters
        ----------
        project: str
            The project ID e.g. P000000010
        collection: str
            The collection ID e.g. C000000001
        repository: str
            The repository to copy to e.g. Dataverse
        message: dict
            The json input to execute the export

        Returns
        -------
        AttributeValue
            dto.AttributeValue object
        """
        if not check_project_id_format(project):
            raise RuleInputValidationError("invalid project id; eg. P000000001")

        if not check_collection_id_format(collection):
            raise RuleInputValidationError("invalid collection id; eg. C000000001")

        # This rule can only be executed by 'rodsadmin', so validating on that here
        if self.session.username != "rods":
            raise RuleInputValidationError("this function has to be run as 'rods'")

        self.prepare_export(project, collection, repository)
        publish_message("datahub.events_tx", "projectCollection.exporter.requested", json.dumps(message))

    @rule_call
    def __export(self, message, project, collection, repository, amqp_host, amqp_port, amqp_user, amqp_pass):
        """
        Calls the rule to start an export.
        This method is private since it requires a lot of parameters and should not be called directly but
        always via 'export_project_collection'
        """
        return RuleInfo(name="requestExportProjectCollection", get_result=False, session=self.session, dto=None)

    @rule_call
    def prepare_export(self, project, collection, repository):
        """
        Calls the rule to prepare the project collection for the export:
        * Open the project collection for modification
        * Add the 'in-queue-for-export' AVU
        """
        return RuleInfo(name="prepareExportProjectCollection", get_result=False, session=self.session, dto=None)

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
        schema_irods_path = f"/nlmumc/projects/{project_id}/{collection_id}/schema.json"
        if check_file_path_format(schema_irods_path) and is_safe_full_path(schema_irods_path):
            return metadata_json.read_irods_json_file(schema_irods_path)
        raise RuleInputValidationError("invalid schema path provided")

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
        schema_irods_path = f"/nlmumc/projects/{project_id}/{collection_id}/.metadata_versions/schema.{version}.json"
        if check_file_path_format(schema_irods_path) and is_safe_full_path(schema_irods_path):
            return metadata_json.read_irods_json_file(schema_irods_path)
        raise RuleInputValidationError("invalid schema path provided")

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
        instance_irods_path = f"/nlmumc/projects/{project_id}/{collection_id}/instance.json"
        if check_file_path_format(instance_irods_path) and is_safe_full_path(instance_irods_path):
            return metadata_json.read_irods_json_file(instance_irods_path)
        raise RuleInputValidationError("invalid instance path provided")

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
        instance_irods_path = (
            f"/nlmumc/projects/{project_id}/{collection_id}/.metadata_versions/instance.{version}.json"
        )
        if check_file_path_format(instance_irods_path) and is_safe_full_path(instance_irods_path):
            return metadata_json.read_irods_json_file(instance_irods_path)
        raise RuleInputValidationError("invalid instance path provided")  # Raise different error

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
        if not check_project_id_format(project_id):
            raise RuleInputValidationError("invalid project id; eg. P000000001")

        if not check_collection_id_format(collection_id):
            raise RuleInputValidationError("invalid collection id; eg. C000000001")

        expected_values = ["false", "true"]
        if open_collection not in expected_values and close_collection not in expected_values:
            raise RuleInputValidationError(
                "invalid value for *open_collection/close_collection: expected 'true' or 'false'"
            )
        return RuleInfo(name="setCollectionSize", get_result=False, session=self.session, dto=None)

    @rule_call
    def create_collection_metadata_snapshot(self, project_id, collection_id):
        """

        Parameters
        ----------
        project_id: str
            The project ID ie P000000001
        collection_id: str
            The collection ID ie C000000001
        """
        if not check_project_id_format(project_id):
            raise RuleInputValidationError("invalid project id; eg. P000000001")

        if not check_collection_id_format(collection_id):
            raise RuleInputValidationError("invalid collection id; eg. C000000001")
        return RuleInfo(name="create_collection_metadata_snapshot", get_result=False, session=self.session, dto=None)

    def save_metadata_json_to_collection(self, project_id, collection_id, instance, schema_dict):
        """
        After a user edits the collection metadata, this method takes care of metadata saving workflow:
            * Create a snapshot of the current collection metadata
            * Overwrite the current instance with the new one
            * Check if we need to overwrite the schema, if yes do it
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
        """
        if not check_project_id_format(project_id):
            raise RuleInputValidationError("invalid project id; eg. P000000001")

        if not check_collection_id_format(collection_id):
            raise RuleInputValidationError("invalid collection id; eg. C000000001")

        self.update_edit_instance(instance, project_id, collection_id)

        collection_path = f"/nlmumc/projects/{project_id}/{collection_id}"
        schema_irods_path = f"{collection_path}/schema.json"
        instance_irods_path = f"{collection_path}/instance.json"

        metadata_json = MetadataJSON(self.session)
        metadata_json.write_instance(instance, instance_irods_path)
        if schema_dict["overwrite"]:
            metadata_json.write_schema(schema_dict["schema_path"], schema_irods_path)

        self.set_collection_avu(collection_path, "schemaVersion", schema_dict["schema_version"])
        self.set_collection_avu(collection_path, "schemaName", schema_dict["schema_file_name"])
        self.set_collection_avu(collection_path, "title", schema_dict["title"])
        self.create_collection_metadata_snapshot(project_id, collection_id)

        # Re-calculate the collection, update the size AVU and close the project collection ACL.
        self.set_collection_size(project_id, collection_id, "false", "false")

    def update_edit_instance(self, instance, project_id, collection_id):
        """
        Some instance values need to be update after an edit

        Parameters
        ----------
        instance: dict
            The json formatted instance data to update
        project_id: str
            The project ID ie P000000001
        collection_id: str
            The collection ID ie C000000001
        """
        collection_path = f"/nlmumc/projects/{project_id}/{collection_id}"
        handle = self.get_collection_attribute_value(collection_path, "PID").value
        if handle != "":
            handle_url = "https://hdl.handle.net/" + handle
            instance["1_Identifier"]["datasetIdentifier"]["@value"] = handle_url
            instance["@id"] = handle_url

        # Set identifier type to "handle"
        instance["1_Identifier"]["datasetIdentifierType"]["rdfs:label"] = "Handle"
        instance["1_Identifier"]["datasetIdentifierType"]["@id"] = "http://vocab.fairdatacollective.org/gdmt/Handle"

        # Overwriting the schema:isBasedOn with the MDR schema handle URL
        schema_url = f"{os.environ['VIRTUAL_HOST']}/hdl/{project_id}/{collection_id}/schema"
        instance["schema:isBasedOn"] = schema_url

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
        if not check_project_id_format(project_id):
            raise RuleInputValidationError("invalid project id; eg. P000000001")

        if not check_collection_id_format(collection_id):
            raise RuleInputValidationError("invalid collection id; eg. C000000001")

        if not isinstance(user, str):
            raise RuleInputValidationError("invalid type for *user: expected a string")

        expected_values = ["false", "true"]
        if open_acl not in expected_values and close_acl not in expected_values:
            raise RuleInputValidationError("invalid value for *open_acl/close_acl: expected 'true' or 'false'")

        return RuleInfo(name="set_acl_for_metadata_snapshot", get_result=False, session=self.session, dto=None)
