from irodsrulewrapper.decorator import rule_call
from irodsrulewrapper.utils import BaseRuleManager, RuleInfo
from irodsrulewrapper.dto.resources import Resources


class ResourceRuleManager(BaseRuleManager):
    def __init__(self, client_user=None):
        BaseRuleManager.__init__(self, client_user)

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
