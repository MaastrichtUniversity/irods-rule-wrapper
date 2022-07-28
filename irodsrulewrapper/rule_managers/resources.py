"""This module contains the ResourceRuleManager class."""
from dhpythonirodsutils import validators, exceptions

from irodsrulewrapper.decorator import rule_call
from irodsrulewrapper.dto.boolean import Boolean
from irodsrulewrapper.dto.collection_sizes import CollectionSizes
from irodsrulewrapper.dto.resources import Resources
from irodsrulewrapper.utils import BaseRuleManager, RuleInfo, RuleInputValidationError


class ResourceRuleManager(BaseRuleManager):
    """This class bundles the resource related wrapped rules methods."""

    def __init__(self, client_user=None, admin_mode=False):
        BaseRuleManager.__init__(self, client_user, admin_mode=admin_mode)

    @rule_call
    def get_ingest_resources(self):
        """
        Get the list of ingest resources

        Returns
        -------
        Resources
            dto.Resources object
        """

        return RuleInfo(name="getIngestResources", get_result=True, session=self.session, dto=Resources)

    @rule_call
    def get_destination_resources(self):
        """
        Get the list of destination resources

        Returns
        -------
        Resources
            dto.Resources object
        """

        return RuleInfo(name="getDestinationResources", get_result=True, session=self.session, dto=Resources)

    @rule_call
    def list_destination_resources_status(self):
        """
        Lists the destination resources and their statuses

        Returns
        -------
        Resources
            The resources

        """

        return RuleInfo(name="list_destination_resources_status", get_result=True, session=self.session, dto=Resources)

    @rule_call
    def get_collection_size_per_resource(self, project):
        """
        List collection size per resource

        Parameters
        project : str
            Project ID
        -------

        Returns
        -------

        """
        try:
            validators.validate_project_id(project)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("invalid project id; eg. P000000001") from err

        return RuleInfo(
            name="get_collection_size_per_resource", get_result=True, session=self.session, dto=CollectionSizes
        )

    @rule_call
    def get_project_resource_availability(self, project_id, ingest, destination, archive):
        """
        Get if a project's resource(s) is/are up

        Parameters
        ----------
        project_id: str
            The project id, ie 'P000000010'
        ingest: str
            If we need to check the 'ingestResource' attribute of the project as well, default True
        destination: str
            If we need to check the 'resource' attribute of the project as well, default True
        archive: str
            If we need to check the 'archiveDestinationResource' attribute of the project as well, default True

        Returns
        -------
        bool
            If the resource(s) to check are both not down, we return True
        """
        try:
            validators.validate_project_id(project_id)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("invalid project id; eg. P000000001") from err

        try:
            validators.validate_string_boolean(ingest)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("invalid value for *ingest: expected 'true' or 'false'") from err

        try:
            validators.validate_string_boolean(destination)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("invalid value for *destination: expected 'true' or 'false'") from err

        try:
            validators.validate_string_boolean(archive)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("invalid value for *archive: expected 'true' or 'false'") from err

        return RuleInfo(name="get_project_resource_availability", get_result=True, session=self.session, dto=Boolean)

    @rule_call
    def get_temporary_password_lifetime(self):
        """
        Query the temporary password lifetime in the server configuration

        Returns
        -------
        str
            Life time of temporary password in seconds
        """
        return RuleInfo(
            name="get_temporary_password_lifetime",
            get_result=True,
            session=self.session,
            dto=None,
            parse_to_dto=self.parse_to_dto,
        )
