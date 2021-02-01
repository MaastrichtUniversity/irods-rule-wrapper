# irods-rule-wrapper
This repository contains the python package with the irods rule logic

### Repository structure

```
< REPOSITORY ROOT >
   |
   |-- irods_rule_wrapper/                 # The root folder of the package
   |    |-- __init__.py                    # Init file containing any properties for the init for the package
   |    |-- decorator.py/                  # Wrapper function to write an iRODS rule call function
   |    |-- rule.py/                       # Contains the RuleManager to open an iRODS connection and the rules functions
   |    |-- TODO/                          # [...]
   |
   |-- tests/                              # 
   |    |
   |    |-- conftest.py                	   # Pytest configuration file
   |    |-- test_example.py                # Example file, all tests should be included in files starting with test for automatic detection
   |
   |-- README.MD                    	   # Repository documentation
   |-- setup.py                            # Setup containing the dependencies and build properties
   |
   |-- ************************************************************************
```

### Installing
Required Python 3.6+ to install with pip from the github repository
```
# From the default branch
pip3 install git+https://github.com/MaastrichtUniversity/irods-rule-wrapper.git

# With ssh
pip3 install git+ssh://github.com/MaastrichtUniversity/irods-rule-wrapper.git

# Or dev-branch
pip3 install git+https://github.com/MaastrichtUniversity/irods-rule-wrapper.git@DHS-1181
```

### Uninstalling

```
pip3 uninstall irods-rule-wrapper
```

### How to use it

```
from irodsrulewrapper.rule import *
import json


rule_manager = RuleManager()

print("Call iRODS rule getUsers")
result = json.loads(rule_manager.get_users("false"))
print(json.dumps(result, indent=4, sort_keys=True))

print("Call iRODS rule getDataStewards")
result = json.loads(rule_manager.get_data_stewards())
print(json.dumps(result, indent=4, sort_keys=True))

print("Call iRODS rule openProjectCollection")
result = rule_manager.open_project_collection("P000000010", "C000000001", "rods", "own")

print("Call iRODS rule closeProjectCollection")
result = rule_manager.close_project_collection("P000000010", "C000000001")

```
