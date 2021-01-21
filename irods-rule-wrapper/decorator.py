from irods.session import iRODSSession
from irods.rule import Rule


def rule_call(func):
    def create_rule_body(*args, **kargs):
        """
        Create a rule body from a template with the list of argument (*args)
            and the list of keyword/named arguments (**kargs)
        Example:
            create_rule_body("P000000010", "C000000001",
                                rule_metadata.name="test_arg", rule_metadata.get_result=True)
        will return
            rule_body='''
            execute_rule{
                test_arg(*arg1, *arg2, *result);
            }
            '''
        """
        rule_metadata = kargs['rule_metadata']
        arguments_string = ""
        for n in range(1, len(args) + 1):
            arguments_string += "*arg" + str(n) + ","

        if rule_metadata.get_result:
            arguments_string = arguments_string + "*result"
        else:
            arguments_string = arguments_string[:-1]

        rule_body = """
        execute_rule{{
        {rule_name}({arguments_string});
        }}
        """.format(rule_name=rule_metadata.name, arguments_string=arguments_string)
        return rule_body

    def create_rule_input(*args, **kargs):
        """
        Create a list of input parameter from the list of argument (*args)
            and the list of keyword/named arguments (**kargs)
        Example:
            create_rule_input("P000000010", "C000000001",
                                rule_metadata.name="test_arg", rule_metadata.get_result=True)
        will return
            {
                "*arg1": '"P000000010"',
                "*arg2": '"C000000001"',
                "*result": '""'
            }
            '''
        """
        rule_metadata = kargs['rule_metadata']
        if rule_metadata.get_result:
            input_params = {"*result": '""'}
        else:
            input_params = {}
        for n in range(1, len(args) + 1):
            key = "*arg" + str(n)
            value = '"{value}"'.format(value=args[n - 1])
            input_params[key] = value
        return input_params

    def execute_rule(rule_body, input_params, get_result):
        session = iRODSSession(host="irods.dh.local", port=1247, user="rods",
                               password="irods", zone='nlmumc')
        output = '*result'
        myrule = Rule(session, body=rule_body,
                      params=input_params, output=output)
        result = myrule.execute()

        if get_result:
            buf = result.MsParam_PI[0].inOutStruct.myStr
            return buf
        return

    # @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        rule_info = func(*args)
        rule_body = create_rule_body(*args, rule_metadata=rule_info)
        input_params = create_rule_input(*args, rule_metadata=rule_info)
        result = execute_rule(rule_body, input_params, rule_info.get_result)
        return result
    return wrapper_decorator