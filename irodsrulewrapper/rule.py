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
from .dto.projects import Projects
from .dto.project import Project
from .dto.collections import Collections
from .dto.drop_zones import DropZones, DropZone
from .dto.contributing_projects import ContributingProjects
from .dto.metadata_xml import MetadataXML
from .dto.token import Token

from .utils import *
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
    def __init__(self, name, get_result, session, dto, input_params=None, rule_body=None):
        self.name = name
        self.get_result = get_result
        self.session = session
        self.dto = dto
        self.input_params = input_params
        self.rule_body = rule_body


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
        # TODO check data format
        if type(authorizationPeriodEndDate) != str:
            raise RuleInputValidationError("invalid type for *authorizationPeriodEndDate: expected a string")

        # TODO check data format
        if type(dataRetentionPeriodEndDate) != str:
            raise RuleInputValidationError("invalid type for *dataRetentionPeriodEndDate: expected a string")

        if type(ingestResource) != str:
            raise RuleInputValidationError("invalid type for *ingestResource: expected a string")

        if type(resource) != str:
            raise RuleInputValidationError("invalid type for *resource: expected a string")

        if type(storageQuotaGb) != int:
            raise RuleInputValidationError("invalid type for *storageQuotaGb: expected an integer")

        if type(title) != str:
            raise RuleInputValidationError("invalid type for *title: expected a string")

        if type(principalInvestigator) != str:
            raise RuleInputValidationError("invalid type for *principalInvestigator: expected a string")

        if type(dataSteward) != str:
            raise RuleInputValidationError("invalid type for *dataSteward: expected a string")

        if type(respCostCenter) != str:
            raise RuleInputValidationError("invalid type for *respCostCenter: expected a string")

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

        if type(username) != str:
            raise RuleInputValidationError("invalid type for *username: expected a string")

        return RuleInfo(name="get_user_group_memberships", get_result=True, session=self.session, dto=Groups)

    @rule_call
    def get_managing_project(self, project_id):
        """
        Query the list of ACL for a project for the client user

        Parameters
        ----------
        project_id : str
            The project's id; e.g P000000010

        Returns
        -------
        ManagingProjects
            The list of usernames for managers, contributors and viewers.
            Returns an empty list if the user is not a manager.
        """
        if not check_project_id_format(project_id):
            raise RuleInputValidationError("invalid project's path format: e.g P000000010")

        return RuleInfo(name="get_managing_project", get_result=True, session=self.session, dto=ManagingProjects)

    @rule_call
    def change_project_permissions(self, project_id, users):
        """
        Change immediately the ACL on the project level.
        Then in the delay queue, change recursively all the collections under the project.

        Parameters
        ----------
        project_id : str
            The project's id; e.g P000000010
        users: str
            The input string to modify the ACL.
            It should follow the following format: 'username:access_level"
            e.g "p.vanschayck@maastrichtuniversity.nl:read m.coonen@maastrichtuniversity.nl:write"
        """
        if not check_project_id_format(project_id):
            raise RuleInputValidationError("invalid project's path format: eg. /nlmumc/projects/P000000010")

        if type(users) != str:
            raise RuleInputValidationError("invalid type for *users: expected a string")

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
    def get_projects_finance(self):
        """
        Get the list of projects financial information

        Returns
        -------
        ProjectsCost
            The list of projects financial information

        """

        return RuleInfo(name="get_projects_finance", get_result=True, session=self.session, dto=ProjectsCost)

    @rule_call
    def get_projects(self):
        """
        Get the list of projects

        Returns
        -------
        Projects
            dto.Projects object
        """
        return RuleInfo(name="list_projects", get_result=True, session=self.session, dto=Projects)

    @rule_call
    def get_project_details(self, project_path):
        """
        Get the list of projects

        Parameters
        ----------
        project_path : str
            The project's absolute path; eg. /nlmumc/projects/P000000010

        Returns
        -------
        Project
            dto.Project object
        """
        if not check_project_path_format(project_path):
            raise RuleInputValidationError("invalid project's path format: eg. /nlmumc/projects/P000000010")

        return RuleInfo(name="get_project_details", get_result=True, session=self.session, dto=Project)

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
    def get_active_drop_zone(self, token, check_ingest_resource_status):
        """
        Get the list of active drop zones

        Parameters
        ----------
        token : str
            The dropzone token
        check_ingest_resource_status : str
            'true'/'false' excepted values; If true, show the project resource status

        Returns
        -------
        DropZone
            dto.DropZone object
        """
        if type(token) != str:
            raise RuleInputValidationError("invalid type for *token: expected a string")

        if check_ingest_resource_status != "false" and check_ingest_resource_status != "true":
            raise RuleInputValidationError("invalid value for *check_ingest_resource_status: expected 'true' or 'false'")

        return RuleInfo(name="get_active_drop_zone", get_result=True, session=self.session, dto=DropZone)

    @rule_call
    def get_contributing_projects(self):
        """
        Query the list of ACL for a project for the client user.
        Returns an empty list if the user is not a contributor.

        Returns
        -------
        ContributingProjects
            dto.ContributingProjects object
        """

        return RuleInfo(name="list_contributing_project", get_result=True, session=self.session, dto=ContributingProjects)

    @rule_call
    def start_ingest(self, user, token):

        input_params = {
            '*user': '"{}"'.format(user),
            '*token': '"{}"'.format(token)
        }

        rule_body = """
            execute_rule{
                ingest;
            }
            """

        return RuleInfo(name="ingest", get_result=False, session=self.session,
                        dto=None, input_params=input_params, rule_body=rule_body)

    @rule_call
    def create_ingest(self, user, token, project, title):

        input_params = {
            '*user': '"{}"'.format(user),
            '*token': '"{}"'.format(token),
            '*project': '"{}"'.format(project),
            '*title': '"{}"'.format(title)
        }

        rule_body = """
        execute_rule{
            createIngest;
        }
        """

        return RuleInfo(name="createIngest", get_result=False, session=self.session,
                        dto=None, input_params=input_params, rule_body=rule_body)

    def create_drop_zone(self, data):
        token = self.generate_token().token
        self.create_ingest(data["user"], token, data["project"], data["title"])
        data["token"] = token
        xml = MetadataXML.create_from_dict(data)
        xml.write_metadata_xml(self.session)

        return token

    def read_metadata_xml(self, token):
        xml = MetadataXML.read_metadata_xml(self.session, token)
        return xml

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
