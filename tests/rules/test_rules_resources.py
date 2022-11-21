from irodsrulewrapper.rule import RuleManager


# requires at least two resources up, like `ires-hnas-um` and `ires-ceph-ac`
def test_rule_get_ingest_resources():
    result = RuleManager(admin_mode=True).get_ingest_resources()
    resources = result.resources
    assert resources is not None
    assert resources.__len__() >= 1
    assert resources[0].name is not None
    assert resources[0].comment is not None


# requires at least two resources up, like `ires-hnas-um` and `ires-ceph-ac`
def test_rule_get_destination_resources():
    result = RuleManager(admin_mode=True).get_destination_resources()
    resources = result.resources
    assert resources is not None
    assert resources.__len__() >= 1
    assert resources[0].name is not None
    assert resources[0].comment is not None


def test_list_destination_resources_status():
    result = RuleManager(admin_mode=True).list_destination_resources_status()
    resources = result.resources
    assert resources is not None


def test_get_collection_size_per_resource():
    result = RuleManager(admin_mode=True).get_collection_size_per_resource("P000000010")
    resources = result.resources_set
    assert resources is not None


def test_get_project_resource_availability():
    result = RuleManager(admin_mode=True).get_project_resource_availability("P000000010", "true", "false", "false")
    status = result.boolean
    assert status is False
