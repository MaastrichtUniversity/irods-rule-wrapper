# irods-rule-wrapper tests
PyTest 


### PyCharm configuration for irods rules call
To be able to execute a rule during a test in PyCharm, we need to set up some irods environment variables:
```
IRODS_HOST=irods.dh.local;IRODS_USER=rods;IRODS_PASS=irods;IRODS_CLIENT_SERVER_POLICY=CS_NEG_REQUIRE;CACHE_TTL_VALUE=86400
```
Click on: Run > Edit configurations > Edit configuration templates > Python tests > pytest

There you can define the default "Environment variables" that will be passed on for each new pytest run configuration

Additionally, some of these tests expect the following to pass:
* `icat` up
* `ires` up
* `keycloak` execution followed by `sram-sync` execution (wait for keycloak to finish before `up`ing `sram-sync`!)
* a second resource up (e.g. `ires-s3-1`)
* `irods.dh.local` needs to point to localhost in your `/etc/hosts` (so the hostname in the SSL cert matches)

To accomplish this, you can do:
```
$ ./rit.sh up -d irods ires ires-s3-1
$ ./rit.sh up -d keycloak
   ... wait for it to finish ...
$ ./rit.sh up -d sram-sync
```
And add this to `/etc/hosts`:
```
127.0.0.1	irods.dh.local
```

Alternatively, if you install pytest-dotenv you can set the environment variables creating a .env file in the tests folder.
```shell script
IRODS_HOST=irods.dh.local
IRODS_USER=rods
IRODS_PASS=irods
IRODS_CLIENT_SERVER_POLICY=CS_NEG_REQUIRE
CACHE_TTL_VALUE=86400
```


### Run the tests in PyCharm

* All the tests: Right-click on the sub folder irods-rule-wrapper/tests and then "Run 'pytest in tests"
* A single test file: Right-click on the file/or in the text editor and then "Run 'pytest in {filename}"
* A single method: Left-click on the green arrow on the left bar next to the line number.