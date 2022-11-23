# irods-rule-wrapper tests

:warning: FIXME: Due to a refactor of iCAT's `bootstrap_irods.sh`, projects
P0..10 and P0..11 are no longer created as they used to and more than a few
tests a broken here. :warning:

### PyCharm configuration for irods rules call
To be able to execute a rule during a test in PyCharm, we need to set up some irods environment variables:
```
IRODS_HOST=icat.dh.local;IRODS_USER=rods;IRODS_PASS=irods;IRODS_CLIENT_SERVER_POLICY=CS_NEG_REQUIRE;CACHE_TTL_VALUE=86400
```
Click on: Run > Edit configurations > Edit configuration templates > Python tests > pytest

There you can define the default "Environment variables" that will be passed on for each new pytest run configuration

Additionally, some of these tests expect the following to pass:
* `icat` up
* `ires` up
* `keycloak` execution followed by `sram-sync` execution (wait for keycloak to finish before `up`ing `sram-sync`!)
* a second resource up (e.g. `ires-ceph-ac`)
* `icat.dh.local` needs to point to localhost in your `/etc/hosts` (so the hostname in the SSL cert matches)

To accomplish this, you can do:
```
$ ./rit.sh up -d icat ires-hnas-um ires-ceph-ac
$ ./rit.sh up -d keycloak
   ... wait for it to finish ...
$ ./rit.sh up -d sram-sync
```
And add this to `/etc/hosts`:
```
127.0.0.1	icat.dh.local
```

### Run the tests in PyCharm

* All the tests: Right-click on the sub folder irods-rule-wrapper/tests and then "Run 'pytest in tests"
* A single test file: Right-click on the file/or in the text editor and then "Run 'pytest in {filename}"
* A single method: Left-click on the green arrow on the left bar next to the line number.


### Run test without PyCharm (in CLI)

Make sure you have this:
`/etc/hosts`:
```
127.0.0.1	icat.dh.local
```

Set up iRODS dev environment expected from the tests
```
# You probably want to make sure that you are on the right branch on all repos,
# And that you're starting from a "clean" slate: ./rit.sh down
$ cd ~docker-dev/
$ ./rit.sh up -d icat
# Wait a bit.. (due to concurrecnty bug, soon to be fixed..)
$ ./rit.sh up -d ires-hnas-um ires-ceph-ac
#  .. maybe wait ..
$ ./rit.sh up -d keycloak   # do we need this?
   ... wait for it to finish ...
$ ./rit.sh up -d sram-sync  # do we need this?
```

Set up irods-rule-wrapper virtual environment for tests
```
$ cd docker-dev/externals/irods-rule-wrapper/
$ mkdir -p venv
$ python -m venv venv/tests-venv
$ source venv/tests-venv/bin/activate
```

Run tests
```
$ export IRODS_HOST=icat.dh.local; export IRODS_USER=rods; export IRODS_PASS=irods; export IRODS_CLIENT_SERVER_POLICY=CS_NEG_REQUIRE; export CACHE_TTL_VALUE=86400; export RIT_ENV=dev
# (venv: tests-env) (cwd: ~docker-dev/externals/irods-rule-wrapper)
$ pytest tests/rules/
# Or for indivitual ones
$ pytest tests/rules/test_drop_zones.py
# Or..
$ pytest tests/rules/test_drop_zones.py::test_generate_token

```

Note: you might need to install pytest
