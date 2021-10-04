from irodsrulewrapper.decorator import rule_call
from irodsrulewrapper.utils import BaseRuleManager, RuleInfo, RuleInputValidationError
from irodsrulewrapper.dto.groups import Groups
from irodsrulewrapper.dto.users import Users


class GroupRuleManager(BaseRuleManager):
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
        if show_service_accounts != "false" and show_service_accounts != "true":
            raise RuleInputValidationError("invalid value for *showServiceAccounts: expected 'true' or 'false'")
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
        if show_special_groups != "false" and show_special_groups != "true":
            raise RuleInputValidationError("invalid value for *showServiceAccounts: expected 'true' or 'false'")

        if type(username) != str:
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
        return RuleInfo(name="getUsersInGroup", get_result=True, session=self.session, dto=Users)

    @rule_call
    def list_groups_users(self):
        """
        Get the list of users for each group

        Returns
        -------
        dict
            JSON rule output
        """

        # TODO Create the DTO

        return RuleInfo(
            name="listGroupsByUser", get_result=True, session=self.session, dto=None, parse_to_dto=self.parse_to_dto
        )
