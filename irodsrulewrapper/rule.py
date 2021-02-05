from irodsrulewrapper.decorator import rule_call
from irods.session import iRODSSession

from .dto.groups import Groups
import json
import os


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

    @rule_call
    def get_users(self, showServiceAccounts):
        return RuleInfo(name="getUsers", get_result=True, session=self.session, dto=None)

    @rule_call
    def get_groups(self, showSpecialGroups):
        return RuleInfo(name="getGroups", get_result=True, session=self.session, dto=Groups)

    @rule_call
    def get_data_stewards(self):
        return RuleInfo(name="getDataStewards", get_result=True, session=self.session, dto=None)

    @rule_call
    def open_project_collection(self, project, project_collection, user, rights):
        # Do input validation here
        return RuleInfo(name="openProjectCollection", get_result=False, session=self.session, dto=None)

    @rule_call
    def close_project_collection(self, project, project_collection):
        # Do input validation here
        return RuleInfo(name="closeProjectCollection", get_result=False, session=self.session, dto=None)

