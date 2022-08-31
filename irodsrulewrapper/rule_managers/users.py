"""This module contains the UserRuleManager class."""
from dhpythonirodsutils import validators, exceptions
from irodsrulewrapper.cache import CacheTTL
from irodsrulewrapper.decorator import rule_call
from irodsrulewrapper.dto.attribute_value import AttributeValue
from irodsrulewrapper.dto.boolean import Boolean
from irodsrulewrapper.dto.data_stewards import DataStewards
from irodsrulewrapper.dto.group import Group
from irodsrulewrapper.dto.user_or_group import UserOrGroup
from irodsrulewrapper.dto.users import Users, User
from irodsrulewrapper.utils import BaseRuleManager, RuleInfo, RuleInputValidationError


class UserRuleManager(BaseRuleManager):
    """This class bundles the user related wrapped rules methods."""

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

        try:
            validators.validate_string_boolean(show_service_accounts)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError(
                "invalid value for *show_service_accounts: expected 'true' or 'false'"
            ) from err

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
        if not isinstance(username, str):
            raise RuleInputValidationError("invalid type for *username: expected a string")
        if not isinstance(attribute, str):
            raise RuleInputValidationError("invalid type for *attribute: expected a string")

        try:
            validators.validate_string_boolean(fatal)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("invalid value for *fatal: expected 'true' or 'false'") from err

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
        if not isinstance(username, str):
            raise RuleInputValidationError("invalid type for *username: expected a string")
        if not isinstance(attribute, str):
            raise RuleInputValidationError("invalid type for *attribute: expected a string")
        if not isinstance(value, str):
            raise RuleInputValidationError("invalid type for *value: expected a string")

        return RuleInfo(name="set_user_attribute_value", get_result=False, session=self.session, dto=None)

    def get_user_or_group(self, uid: str):
        """
        Retrieve a user or group DTO based on the input uid.
        First check if the uid is present the cached dict. Otherwise, query the uid.

        Parameters
        ----------
        uid: str
            The uid to query and retrieve from the cache

        Returns
        -------
        User|Group
            The DTO of the input uid
        """
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
        """
        Get user or group information from its id

        Parameters
        ----------
        uid : str
            The account's id; eg.g '10132'

        Returns
        -------
        UserOrGroup
            Simple DTO that contains the result of the rule
        """
        if not isinstance(uid, str):
            raise RuleInputValidationError("invalid type for *uid: expected a string")

        return RuleInfo(name="get_user_or_group_by_id", get_result=True, session=self.session, dto=UserOrGroup)

    @rule_call
    def get_user_internal_affiliation_status(self, username):
        """
        Get the user voPersonExternalID and check if the user is part of the UM or MUMC organization.

        Parameters
        ----------
        username: str
            The user to check

        Returns
        -------
        bool
            True, if the user is from the UM or MUMC organization. Otherwise, False.
        """
        if not isinstance(username, str):
            raise RuleInputValidationError("invalid type for *username: expected a string")

        return RuleInfo(name="get_user_internal_affiliation_status", get_result=True, session=self.session, dto=Boolean)

    @rule_call
    def get_temporary_password_lifetime(self):
        """
        Query the temporary password lifetime in the server configuration

        Returns
        -------
        int
            Life time of temporary password in seconds
        """
        return RuleInfo(
            name="get_temporary_password_lifetime",
            get_result=True,
            session=self.session,
            dto=None,
            parse_to_dto=self.parse_to_dto,
        )
