"""This module contains the UserRuleManager class."""
from dhpythonirodsutils import validators, exceptions

from irodsrulewrapper.decorator import rule_call
from irodsrulewrapper.dto.active_processes import ActiveProcesses
from irodsrulewrapper.dto.attribute_value import AttributeValue
from irodsrulewrapper.dto.boolean import Boolean
from irodsrulewrapper.dto.data_stewards import DataStewards
from irodsrulewrapper.dto.user_or_group import UserOrGroup
from irodsrulewrapper.dto.users import Users
from irodsrulewrapper.dto.users_groups_expanded import UsersGroupsExpanded
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

    @rule_call
    def get_user_or_group_by_id(self, uid):
        """
        Get user or group information from its id

        Parameters
        ----------
        uid : str
            The account's id; e.g: '10132'

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

    def get_expanded_user_group_information(self, users: set):
        """
        Wrapper around private function so user can just provide a list to the method
        Functionality: see _get_expanded_user_group_information

        Parameters
        ----------
        users: set
            A list of participants to get the information from

        Returns
        -------
        dict
            A dictionary (unique) with all users and their emails and display names and groups and their display name
        """
        users = ";".join(users)
        return self._get_expanded_user_group_information(users)

    @rule_call
    def _get_expanded_user_group_information(self, users: str):
        """
        Get the information (email and display name) about users and groups
        This expands groups to all its users and also gets their emails and display names.

        Parameters
        ----------
        users: str
            A semicolon separated string of users/groups
            (e.g. 'dlinssen;datahub;jmelius')

        Returns
        -------
        UsersGroupsExpanded
            A dictionary (unique) with all users and their emails and display names and groups and their display name
        """
        if not isinstance(users, str):
            raise RuleInputValidationError("invalid type for *users: expected a string")

        return RuleInfo(
            name="get_expanded_user_group_information",
            get_result=True,
            session=self.session,
            dto=UsersGroupsExpanded,
            parse_to_dto=self.parse_to_dto,
        )

    @rule_call
    def get_user_active_processes(self, query_drop_zones, query_archive, query_unarchive):
        """
        Query all the active process status (ingest and  tape archive) of the user.

        Parameters
        ----------
        query_drop_zones: str
            'true'/'false' expected; If true, query the list of active drop_zones & ingest processes
        query_archive: str
            'true'/'false' expected; If true, query the list of active archive
        query_unarchive: str
            'true'/'false' expected; If true, query the list of active un-archive processes

        Returns
        -------
        ActiveProcesses
            a DTO ActiveProcesses object
        """

        try:
            validators.validate_string_boolean(query_drop_zones)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("invalid value for *query_drop_zones: expected 'true' or 'false'") from err

        try:
            validators.validate_string_boolean(query_archive)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("invalid value for *query_archive: expected 'true' or 'false'") from err

        try:
            validators.validate_string_boolean(query_unarchive)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("invalid value for *query_unarchive: expected 'true' or 'false'") from err

        return RuleInfo(name="get_user_active_processes", get_result=True, session=self.session, dto=ActiveProcesses)
