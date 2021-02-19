from irodsrulewrapper.decorator import rule_call
from irods.session import iRODSSession
from irods.exception import CAT_INVALID_CLIENT_USER

from .dto.groups import Groups
from .dto.users import Users
from .dto.data_stewards import DataStewards
from .dto.create_project import CreateProject
from .dto.attribute_value import AttributeValue
from .dto.resources import Resources
from .dto.managing_projects import ManagingProjects
from .dto.projects_cost import ProjectsCost

import os


class RuleInputValidationError(Exception):
    """Exception raised for errors during the rule's validation of the input parameters.

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "RuleInputValidationError, {0}".format(self.message)


class RuleInfo:
    def __init__(self, name, get_result, session, dto):
        self.name = name
        self.get_result = get_result
        self.session = session
        self.dto = dto


class RuleManager:
    def __init__(self, client_user=None):
        if client_user is None:
            self.session = iRODSSession(host=os.environ['IRODS_HOST'], port=1247, user=os.environ['IRODS_USER'],
                                        password=os.environ['IRODS_PASS'], zone='nlmumc')
        else:
            self.session = iRODSSession(host=os.environ['IRODS_HOST'], port=1247, user=os.environ['IRODS_USER'],
                                        password=os.environ['IRODS_PASS'], zone='nlmumc', client_user=client_user)

    def check_irods_connection(self):
        """
        Check if an iRODS connection can be established

        Returns
        -------
        bool
            boolean
        """
        try:
            self.session.pool.get_connection()
        except CAT_INVALID_CLIENT_USER:
            return False
        else:
            return True

    @rule_call
    def get_users(self, show_service_accounts):
        """
        Get the list of users

        Parameters
        ----------
        show_service_accounts : str
            'true'/'false' excepted values; If true, hide the service accounts in the result

        Returns
        -------
        Users
            dto.Users object
        """
        if show_service_accounts != "false" and show_service_accounts != "true":
            raise RuleInputValidationError("invalid value for *showServiceAccounts: expected 'true' or 'false'")
        return RuleInfo(name="getUsers", get_result=True, session=self.session, dto=Users)

    @rule_call
    def get_groups(self, show_service_accounts):
        """
        Get the list of groups

        Parameters
        ----------
        show_service_accounts : str
            'true'/'false' excepted values; If true, hide the special groups in the result

        Returns
        -------
        Groups
            dto.Groups object
        """
        if show_service_accounts != "false" and show_service_accounts != "true":
            raise RuleInputValidationError("invalid value for *showServiceAccounts: expected 'true' or 'false'")
        return RuleInfo(name="getGroups", get_result=True, session=self.session, dto=Groups)

    @rule_call
    def get_data_stewards(self):
        """
        Get the list of data stewards

        Returns
        -------
        DataStewards
            dto.DataStewards object
        """
        return RuleInfo(name="getDataStewards", get_result=True, session=self.session, dto=DataStewards)

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
    def create_new_project(self, authorizationPeriodEndDate, dataRetentionPeriodEndDate,
                       ingestResource, resource, storageQuotaGb, title, principalInvestigator,
                       dataSteward, respCostCenter, openAccess, tapeArchive):
        """
        Create a new iRODS project

        Parameters
        ----------
        authorizationPeriodEndDate : str
            The username
        dataRetentionPeriodEndDate : str
            The username
        ingestResource : str
            The ingest resource to use during the ingestion
        resource : str
            The destination resource to store future collection
        storageQuotaGb  : str
            The storage quota in Gb
        title : str
            The project title
        principalInvestigator : str
            The principal investigator(OBI:0000103) for the project
        dataSteward : str
            The data steward for the project
        respCostCenter : str
            The budget number
        openAccess : str
            'true'/'false' excepted values
        tapeArchive : str
            'true'/'false' excepted values

        Returns
        -------
        CreateProject
            dto.CreateProject object
        """
        # TODO extend parameters validation
        if openAccess != "false" and openAccess != "true":
            raise RuleInputValidationError("invalid value for *openAccess: expected 'true' or 'false'")

        if tapeArchive != "false" and tapeArchive != "true":
            raise RuleInputValidationError("invalid value for *tapeArchive: expected 'true' or 'false'")
        return RuleInfo(name="create_new_project", get_result=True, session=self.session, dto=CreateProject)

    @rule_call
    def get_username_attribute_value(self, username, attribute):
        """
        Query an attribute value from the user list of AVU

        Parameters
        ----------
        username : str
            The username
        attribute : str
            The user attribute to query

        Returns
        -------
        AttributeValue
            dto.AttributeValue object
        """
        if type(username) != str:
            raise RuleInputValidationError("invalid type for *username: expected a string")
        if type(attribute) != str:
            raise RuleInputValidationError("invalid type for *attribute: expected a string")

        return RuleInfo(name="get_username_attribute_value", get_result=True, session=self.session, dto=AttributeValue)

    @rule_call
    def set_acl(self, mode, access_level, user, path):
        """
        Set the ACL of a given collection

        Parameters
        ----------
        mode : str
            'default', 'recursive' excepted values
        access_level : str
            access level: 'own', 'write', 'read'
        user : str
            The username
        path : str
            The absolute path of the collection
        """
        if mode != "default" and mode != "recursive":
            raise RuleInputValidationError("invalid value for *mode: expected 'default' or 'recursive'")
        if access_level != "own" and access_level != "write" and access_level != "read":
            raise RuleInputValidationError("invalid value for *access_level: expected 'default' or 'recursive'")
        if type(user) != str:
            raise RuleInputValidationError("invalid type for *user: expected a string")
        if type(path) != str:
            raise RuleInputValidationError("invalid type for *path: expected a string")

        return RuleInfo(name="set_acl", get_result=False, session=self.session, dto=None)

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
    def get_user_group_memberships(self, show_special_groups, username):
        """
        Get the group membership of a given user

        Parameters
        ----------
        show_special_groups : str
            'true'/'false' excepted values; If true, hide the special groups in the result
        username : str
            The username to use for the query

        Returns
        -------
        Groups
            dto.Groups object
        """
        if show_special_groups != "false" and show_special_groups != "true":
            raise RuleInputValidationError("invalid value for *showServiceAccounts: expected 'true' or 'false'")

        return RuleInfo(name="get_user_group_memberships", get_result=True, session=self.session, dto=Groups)

    @rule_call
    def get_managing_project(self, project_id):
        """
        Query the list of ACL for a project for the client user

        Parameters
        ----------
        project_id : str
            The project's id; eg.g P000000010

        Returns
        -------
        dict
            The list of usernames for managers, contributors and viewers.
            Returns an empty list if the user is not a manager.
        """

        return RuleInfo(name="get_managing_project", get_result=True, session=self.session, dto=ManagingProjects)

    @rule_call
    def change_project_permissions(self, project_id, users):
        """
        Change immediately the ACL on the project level.
        Then in the delay queue, change recursively all the collections under the project.

        Parameters
        ----------
        project_id : str
            The project's id; eg.g P000000010
        users: str
            The input string to modify the ACL.
            It should follow the following format: 'username:access_level"
            e.g "p.vanschayck@maastrichtuniversity.nl:read m.coonen@maastrichtuniversity.nl:write"
        """

        return RuleInfo(name="changeProjectPermissions", get_result=False, session=self.session, dto=None)

    @rule_call
    def set_collection_avu(self, collection_path, attribute, value):
        """
        Set a collection AVU

        Parameters
        ----------
        collection_path : str
            The collection's absolute path; eg. /nlmumc/projects/P000000001
        attribute: str
            The attribute that is going to be set; eg. 'responsibleCostCenter'
        value: str
            The value that is going to bet set; eg. 'UM-12345678N'
        """

        return RuleInfo(name="setCollectionAVU", get_result=False, session=self.session, dto=None)

    @rule_call
    def get_projects_finance(self):
        """
        Get the list of projects financial information

        Returns
        -------
        dict
            The list of projects financial information

        """

        return RuleInfo(name="get_projects_finance", get_result=True, session=self.session, dto=ProjectsCost)




