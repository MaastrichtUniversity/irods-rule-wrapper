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
Required Python 3.10+ to install with pip from the github repository. DTOs use Pydantic 2; use
`model_dump()` and `model_dump_json()` to serialize them.
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

Collection metadata saves require the matching `save_collection_metadata` rule
from irods-ruleset. Deploy that ruleset before updating application workers.
The server assigns versioned identifiers and writes each document once before
creating its snapshot; the existing snapshot rule remains available to callers.
The submitted payload is staged in the caller's iRODS home and removed when the
save call finishes, including on failure.

`irods_session_scope()` shares sessions within one scope and closes them on
exit. HTTP applications can opt into reuse across requests:

```python
from irodsrulewrapper.rule import RuleManager
from irodsrulewrapper.session_pool import get_irods_session_pool
from irodsrulewrapper.utils import irods_session_scope

with irods_session_scope(pool=get_irods_session_pool()):
    rule_manager = RuleManager("username")
    # Use borrowed managers only within this scope.
```

The worker-local pool retains up to 32 idle sessions, separated by identity and
connection settings. Idle sessions expire after 60 seconds; expiry is checked
on borrowing and returning, so inactive workers may retain sockets longer.
Concurrent scopes borrow separate sessions. Cached connections receive a
read-only health check before reuse; application writes are never replayed on
network failure. Call `close_irods_session_pool()` at worker exit (also registered
with `atexit`). Standalone managers keep their existing ownership behavior.

```
from irodsrulewrapper.rule import *
import json


rule_manager = RuleManager(admin_mode=True)

print("Call iRODS rule get_users")
result = json.loads(rule_manager.get_users("false"))
print(json.dumps(result, indent=4, sort_keys=True))

print("Call iRODS rule get_data_stewards")
result = json.loads(rule_manager.get_data_stewards())
print(json.dumps(result, indent=4, sort_keys=True))

print("Call iRODS rule openProjectCollection")
result = rule_manager.open_project_collection("P000000010", "C000000001", "rods", "own")

print("Call iRODS rule closeProjectCollection")
result = rule_manager.close_project_collection("P000000010", "C000000001")

```
