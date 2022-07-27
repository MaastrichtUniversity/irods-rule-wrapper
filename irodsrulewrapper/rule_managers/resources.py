from irodsrulewrapper.decorator import rule_call
from irodsrulewrapper.utils import BaseRuleManager, RuleInfo, RuleInputValidationError
from irodsrulewrapper.dto.resources import Resources
from irodsrulewrapper.dto.boolean import Boolean
from irodsrulewrapper.dto.collection_sizes import CollectionSizes

from dhpythonirodsutils import validators, exceptions


class ResourceRuleManager(BaseRuleManager):
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
        List cllection size per resource

        Parameters
        project : str
            Project ID
        -------

        Returns
        -------

        """
        try:
            validators.validate_project_id(project)
        except exceptions.ValidationError:
            raise RuleInputValidationError("invalid project id; eg. P000000001")

        return RuleInfo(
            name="get_collection_size_per_resource", get_result=True, session=self.session, dto=CollectionSizes
        )

    @rule_call
    def get_project_resource_availability(self, project_id, ingest, destination, archive):
        """

        Parameters
        ----------
        project_id
        ingest
        destination
        archive

        Returns
        -------

        """
        try:
            validators.validate_project_id(project_id)
        except exceptions.ValidationError:
            raise RuleInputValidationError("invalid project id; eg. P000000001")

        return RuleInfo(name="get_project_resource_availability", get_result=True, session=self.session, dto=Boolean)

    @rule_call
    def get_temporary_password_lifetime(self):
        """

        Parameters
        ----------

        Returns
        -------
        Life time of temporary password in seconds
        """
        return RuleInfo(name="get_temporary_password_lifetime", get_result=True, session=self.session, dto=None, parse_to_dto=self.parse_to_dto)
