from irods.session import iRODSSession
from irods.rule import Rule
import json


def rule_call(func):
    def create_rule_body(*args, **kargs):
        """
        Create a rule body from a template with the list of arguments (*args)
            and the list of keyword/named arguments (**kargs)
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
        rule_info = kargs['rule_info']
        arguments_string = ""
        for n in range(2, len(args) + 1):
            arguments_string += "*arg" + str(n) + ","

        if rule_info.get_result:
            arguments_string = arguments_string + "*result"
        else:
            arguments_string = arguments_string[:-1]

        rule_body = """
        execute_rule{{
        {rule_name}({arguments_string});
        }}
        """.format(rule_name=rule_info.name, arguments_string=arguments_string)
        return rule_body

    def create_rule_input(*args, **kargs):
        """
        Create a list of input parameter from the list of arguments (*args)
            and the list of keyword/named arguments (**kargs)
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
        rule_info = kargs['rule_info']
        if rule_info.get_result:
            input_params = {"*result": '""'}
        else:
            input_params = {}
        for n in range(2, len(args) + 1):
            key = "*arg" + str(n)
            value = '"{value}"'.format(value=args[n - 1])
            input_params[key] = value
        return input_params

    def execute_rule(rule_body, input_params, rule_info):
        myrule = Rule(rule_info.session, body=rule_body,
                      params=input_params, output='*result')
        result = myrule.execute()
        if rule_info.get_result:
            buf = result.MsParam_PI[0].inOutStruct.myStr
            buf_json = json.loads(buf)
            result = rule_info.dto.create_from_rule_result(buf_json)
            return result
        return

    def wrapper_decorator(*args, **kwargs):
        rule_info = func(*args)
        rule_body = create_rule_body(*args, rule_info=rule_info)
        input_params = create_rule_input(*args, rule_info=rule_info)
        result = execute_rule(rule_body, input_params, rule_info)
        return result
    return wrapper_decorator
