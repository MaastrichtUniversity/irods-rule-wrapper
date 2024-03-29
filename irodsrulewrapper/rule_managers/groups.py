"""This module contains the GroupRuleManager class."""
from dhpythonirodsutils import validators, exceptions

from irodsrulewrapper.decorator import rule_call
from irodsrulewrapper.dto.groups import Groups
from irodsrulewrapper.dto.users import Users

from irodsrulewrapper.utils import BaseRuleManager, RuleInfo, RuleInputValidationError


class GroupRuleManager(BaseRuleManager):
    """This class bundles the group related wrapped rules methods."""

    def __init__(self, client_user=None, admin_mode=False):
        BaseRuleManager.__init__(self, client_user, admin_mode=admin_mode)

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
        try:
            validators.validate_string_boolean(show_service_accounts)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError(
                "invalid value for *showServiceAccounts: expected 'true' or 'false'"
            ) from err
        return RuleInfo(name="get_groups", get_result=True, session=self.session, dto=Groups)

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
        try:
            validators.validate_string_boolean(show_special_groups)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError(
                "invalid value for *showServiceAccounts: expected 'true' or 'false'"
            ) from err

        if not isinstance(username, str):
            raise RuleInputValidationError("invalid type for *username: expected a string")

        return RuleInfo(name="get_user_group_memberships", get_result=True, session=self.session, dto=Groups)

    @rule_call
    def get_users_in_group(self, group_id):
        """
        Get the list of users in a specific group

        Parameters
        ----------
        group_id : str
            Group id

        Returns
        -------
        Users
            dto.Users object
        """
        if not group_id.isdigit():
            raise RuleInputValidationError("invalid value for *group_id: expected an integer as string")

        return RuleInfo(name="getUsersInGroup", get_result=True, session=self.session, dto=Users)
