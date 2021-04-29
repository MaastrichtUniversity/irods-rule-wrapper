from irodsrulewrapper.decorator import rule_call
from irodsrulewrapper.utils import check_project_path_format, check_project_collection_path_format, \
    check_project_id_format, check_collection_id_format, BaseRuleManager, RuleInfo, RuleInputValidationError
from irodsrulewrapper.dto.collections import Collections, Collection


class CollectionRuleManager(BaseRuleManager):
    def __init__(self):
        BaseRuleManager.__init__(self)

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

        return RuleInfo(name="detailsProjectCollection", get_result=True, session=self.session, dto=Collection)
