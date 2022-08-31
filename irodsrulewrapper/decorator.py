"""
This module contains the decorator function to execute iRODS rule
"""
import json
from typing import Callable

from irods.rule import Rule


def rule_call(func: Callable):
    """
    This function extends another function, by parsing its input function arguments and its output RuleInfo, to execute
    it as an iRODS rule.

    Extending the input function:
        * execute the input function body (must contain input validation)
        * parse the output RuleInfo
        * prepare the rule object and then execute it
        * either parse the rule result as a DTO or pass the result JSON object
        * return the result to the caller.

    Examples
    --------
        @rule_call
        def get_groups(self, show_service_accounts):
            try:
                validators.validate_string_boolean(show_service_accounts)
            except exceptions.ValidationError as err:
                raise RuleInputValidationError(
                    "invalid value for *showServiceAccounts: expected 'true' or 'false'"
                ) from err

            return RuleInfo(name="get_groups", get_result=True, session=self.session, dto=Groups)

    is equivalent to:

        def get_groups(self, show_service_accounts):
            try:
                validators.validate_string_boolean(show_service_accounts)
            except exceptions.ValidationError as err:
                raise RuleInputValidationError(
                    "invalid value for *showServiceAccounts: expected 'true' or 'false'"
                ) from err

            rule_info = RuleInfo(name="get_groups", get_result=True, session=self.session, dto=Groups)
            rule_body = create_rule_body(show_service_accounts, rule_info=rule_info)
            input_params = create_rule_input(show_service_accounts, rule_info=rule_info)
            result = execute_rule(rule_body, input_params, rule_info)

            return result

    the caller just need to execute:
        result = RuleManager("user").get_groups("false")

    Parameters
    ----------
    func: Callable
        The function to decorate to be executed as a rule

    Returns
    -------
    Any
        The rule result as the mentioned DTO or a JSON
    """

    def create_rule_body(*args, **kwargs):
        """
        Create a rule body from a template with the list of arguments (*args)
            and the list of keyword/named arguments (**kwargs)
        Example:
            create_rule_body("P000000010", "C000000001",
                                rule_info.name="test_arg", rule_info.get_result=True)
        will return
            rule_body='''
            execute_rule{
                test_arg(*arg1, *arg2, *result);
            }
            '''
        """
        rule_info = kwargs["rule_info"]
        arguments_string = ""
        for argument_index in range(2, len(args) + 1):
            arguments_string += "*arg" + str(argument_index) + ","

        if rule_info.get_result:
            arguments_string = arguments_string + "*result"
        else:
            arguments_string = arguments_string[:-1]

        rule_body = f"""
        execute_rule{{
        {rule_info.name}({arguments_string});
        }}
        """
        return rule_body

    def create_rule_input(*args, **kwargs):
        """
        Create a list of input parameter from the list of arguments (*args)
            and the list of keyword/named arguments (**kwargs)
        Example:
            create_rule_input("P000000010", "C000000001",
                                rule_info.name="test_arg", rule_info.get_result=True)
        will return
            {
                "*arg1": '"P000000010"',
                "*arg2": '"C000000001"',
                "*result": '""'
            }
            '''
        """
        rule_info = kwargs["rule_info"]
        if rule_info.get_result:
            input_params = {"*result": '""'}
        else:
            input_params = {}
        for argument_index in range(2, len(args) + 1):
            key = "*arg" + str(argument_index)
            value = f'"{args[argument_index - 1]}"'
            input_params[key] = value
        return input_params

    def execute_rule(rule_body, input_params, rule_info):
        myrule = Rule(rule_info.session, body=rule_body, params=input_params, output="*result")
        result = myrule.execute()
        if rule_info.get_result:
            buf = result.MsParam_PI[0].inOutStruct.myStr
            buf_json = json.loads(buf)
            # Check if it will return the JSON rule's output or the DTO
            if rule_info.parse_to_dto:
                return rule_info.dto.create_from_rule_result(buf_json)

            return buf_json

        return None

    def wrapper_decorator(*args):
        rule_info = func(*args)

        if rule_info.rule_body is None:
            rule_body = create_rule_body(*args, rule_info=rule_info)
        else:
            rule_body = rule_info.rule_body

        if rule_info.input_params is None:
            input_params = create_rule_input(*args, rule_info=rule_info)
        else:
            input_params = rule_info.input_params

        result = execute_rule(rule_body, input_params, rule_info)
        return result

    return wrapper_decorator
