# irods-rule-wrapper tests
PyTest 


### PyCharm configuration for irods rules call
To be able to execute a rule during a test in PyCharm, we need to set up some irods environment variables:
```
IRODS_HOST=0.0.0.0;IRODS_USER=rods;IRODS_PASS=irods
```
Click on: Run > Edit configurations > Templates > Python tests > pytest

There you can define the default "Environment variables" that will passed on for each new pytest run configuration

### Run the tests in PyCarm

* All the tests: Right click on the sub folder irods-rule-wrapper/tests and then "Run 'pytest in tests"
* A single test file: Right click on the file/or in the text editor and then "Run 'pytest in {filename}"
* A single method: Left click on the green arrow on the left bar next to the line number.

