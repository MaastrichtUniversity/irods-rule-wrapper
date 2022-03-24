from irodsrulewrapper.decorator import rule_call
from irodsrulewrapper.utils import BaseRuleManager, RuleInfo, RuleInputValidationError
from irodsrulewrapper.dto.users import Users, User
from irodsrulewrapper.dto.group import Group
from irodsrulewrapper.dto.user_or_group import UserOrGroup
from irodsrulewrapper.dto.data_stewards import DataStewards
from irodsrulewrapper.dto.attribute_value import AttributeValue
from irodsrulewrapper.cache import CacheTTL


class UserRuleManager(BaseRuleManager):
    def __init__(self, client_user=None, admin_mode=False):
        BaseRuleManager.__init__(self, client_user=client_user, admin_mode=admin_mode)

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
    def get_user_attribute_value(self, username, attribute, fatal):
        """
        Query an attribute value from the user list of AVU

        Parameters
        ----------
        username : str
            The username
        attribute : str
            The user attribute to query
        fatal : str
            'true'/'false' expected; If true, raise an exception when the query result is empty

        Returns
        -------
        AttributeValue
            dto.AttributeValue object
        """
        if type(username) != str:
            raise RuleInputValidationError("invalid type for *username: expected a string")
        if type(attribute) != str:
            raise RuleInputValidationError("invalid type for *attribute: expected a string")
        if fatal != "false" and fatal != "true":
            raise RuleInputValidationError("invalid value for *fatal: expected 'true' or 'false'")

        return RuleInfo(name="get_user_attribute_value", get_result=True, session=self.session, dto=AttributeValue)

    @rule_call
    def set_user_attribute_value(self, username, attribute, value):
        """
        Set an attribute value to the input user

        Parameters
        ----------
        username : str
            The username
        attribute : str
            The user attribute to set
        value : str
            The user attribute's value to set

        """
        if type(username) != str:
            raise RuleInputValidationError("invalid type for *username: expected a string")
        if type(attribute) != str:
            raise RuleInputValidationError("invalid type for *attribute: expected a string")
        if type(value) != str:
            raise RuleInputValidationError("invalid type for *value: expected a string")

        return RuleInfo(name="set_user_attribute_value", get_result=False, session=self.session, dto=None)

    def get_user_or_group(self, uid):
        if uid not in CacheTTL.CACHE_USERS_GROUPS:
            # TODO Find an another way, as performing, to skip rodsadmin & service-accounts than hard-coded values
            item = self.get_user_or_group_by_id(uid)
            if item.result["account_type"] == "rodsuser":
                CacheTTL.CACHE_USERS_GROUPS[uid] = User.create_from_rule_result(item.result)
            elif item.result["account_type"] == "rodsgroup":
                CacheTTL.CACHE_USERS_GROUPS[uid] = Group.create_from_rule_result(item.result)

        return CacheTTL.CACHE_USERS_GROUPS[uid]

    @rule_call
    def get_user_or_group_by_id(self, uid):
        if type(uid) != str:
            raise RuleInputValidationError("invalid type for *username: expected a string")

        return RuleInfo(name="get_user_or_group_by_id", get_result=True, session=self.session, dto=UserOrGroup)
