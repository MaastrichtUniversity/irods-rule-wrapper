from decorator import rule_call

import json


class RuleInfo:
    name = None
    get_result = None
    def __init__(self, name, get_result):
        self.name= name
        self.get_result= get_result

@rule_call
def get_test_arg(arg1, arg2):
    return RuleInfo(name="test_arg", get_result=True)

@rule_call
def get_users(showServiceAccounts):
    return RuleInfo(name="getUsers", get_result=True)

@rule_call
def get_data_stewards():
    return RuleInfo(name="getDataStewards", get_result=True)

@rule_call
def open_project_collection(project, project_collection, user, rights):
    # Do input validation here
    return RuleInfo(name="openProjectCollection", get_result=False)

@rule_call
def close_project_collection(project, project_collection):
    # Do input validation here
    return RuleInfo(name="closeProjectCollection", get_result=False)


### Test ###

print("Call python rule test_arg")
result = get_test_arg("Testing decorator", "Value from variable")
print(result)

print("\nCall iRODS rule getUsers")
result = json.loads(get_users("false"))
print(json.dumps(result, indent=4, sort_keys=True))

print("\nCall iRODS rule getDataStewards")
result = json.loads(get_data_stewards())
print(json.dumps(result, indent=4, sort_keys=True))

print("\nCall iRODS rule openProjectCollection")
result = open_project_collection("P000000010", "C000000001", "rods", "own")

print("\nCall iRODS rule closeProjectCollection")
result = close_project_collection("P000000010", "C000000001")

