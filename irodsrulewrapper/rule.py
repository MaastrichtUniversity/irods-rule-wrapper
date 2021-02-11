from irodsrulewrapper.decorator import rule_call
from irods.session import iRODSSession
from irods.exception import CAT_INVALID_CLIENT_USER

from .dto.groups import Groups
from .dto.users import Users
from .dto.data_stewards import DataStewards
from .dto.create_project import CreateProject
from .dto.attribute_value import AttributeValue
from .dto.resources import Resources

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
        try:
            self.session.pool.get_connection()
        except CAT_INVALID_CLIENT_USER:
            return False
        else:
            return True

    @rule_call
    def get_users(self, show_service_accounts):
        if show_service_accounts != "false" and show_service_accounts != "true":
            raise RuleInputValidationError("invalid value for *showServiceAccounts: expected 'true' or 'false'")
        return RuleInfo(name="getUsers", get_result=True, session=self.session, dto=Users)

    @rule_call
    def get_groups(self, show_service_accounts):
        if show_service_accounts != "false" and show_service_accounts != "true":
            raise RuleInputValidationError("invalid value for *showServiceAccounts: expected 'true' or 'false'")
        return RuleInfo(name="getGroups", get_result=True, session=self.session, dto=Groups)

    @rule_call
    def get_data_stewards(self):
        return RuleInfo(name="getDataStewards", get_result=True, session=self.session, dto=DataStewards)

    @rule_call
    def open_project_collection(self, project, project_collection, user, rights):
        # Do input validation here
        return RuleInfo(name="openProjectCollection", get_result=False, session=self.session, dto=None)

    @rule_call
    def close_project_collection(self, project, project_collection):
        # Do input validation here
        return RuleInfo(name="closeProjectCollection", get_result=False, session=self.session, dto=None)

    @rule_call
    def create_new_project(self, authorizationPeriodEndDate, dataRetentionPeriodEndDate,
                       ingestResource, resource, storageQuotaGb, title, principalInvestigator,
                       dataSteward, respCostCenter, openAccess, tapeArchive):
        # Do input validation here
        return RuleInfo(name="create_new_project", get_result=True, session=self.session, dto=CreateProject)

    @rule_call
    def get_username_attribute_value(self, username, attribute):
        # Do input validation here
        return RuleInfo(name="get_username_attribute_value", get_result=True, session=self.session, dto=AttributeValue)

    @rule_call
    def set_acl(self, mode, access_level, user, path):
        # Do input validation here
        return RuleInfo(name="set_acl", get_result=False, session=self.session, dto=None)

    @rule_call
    def get_ingest_resources(self):
        return RuleInfo(name="getIngestResources", get_result=True, session=self.session, dto=Resources)

    @rule_call
    def get_destination_resources(self):
        return RuleInfo(name="getDestinationResources", get_result=True, session=self.session, dto=Resources)

    @rule_call
    def get_user_group_memberships(self, show_special_groups, username):
        return RuleInfo(name="get_user_group_memberships", get_result=True, session=self.session, dto=Groups)

