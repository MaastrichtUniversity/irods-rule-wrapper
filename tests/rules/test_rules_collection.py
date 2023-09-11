from irodsrulewrapper.rule import RuleManager, RuleJSONManager


def test_open_project_collection():
    RuleManager(admin_mode=True).open_project_collection("P000000010", "C000000001", "rods", "own")


def test_close_project_collection():
    RuleManager(admin_mode=True).close_project_collection("P000000010", "C000000001")


def test_rule_set_collection_avu():
    RuleManager(admin_mode=True).set_collection_avu("/nlmumc/projects/P000000010/C000000001", "test", "test")


def test_rule_get_collections():
    result = RuleManager(admin_mode=True).get_collections("/nlmumc/projects/P000000011")
    collections = result.collections
    assert collections is not None
    assert collections[0].creator == "irods_bootstrap@docker.dev"


def test_rule_get_project_collection_details():
    collection = RuleManager(admin_mode=True).get_project_collection_details("P000000011", "C000000001", "false")
    assert collection is not None
    assert collection.id == "C000000001"
    assert collection.creator == "irods_bootstrap@docker.dev"
    assert collection.title == "(HVC) Placeholder collection"
    assert collection.enable_archive is False
    assert collection.enable_open_access_export is False


def test_rule_archive_project_collection():
    RuleManager("service-surfarchive").archive_project_collection("/nlmumc/projects/P000000014/C000000002")


def test_rule_unarchive_project_collection():
    RuleManager("service-surfarchive").unarchive_project_collection("/nlmumc/projects/P000000014/C000000002")


def test_rule_get_collection_attribute_value():
    avu = RuleManager(admin_mode=True).get_collection_attribute_value("/nlmumc/projects/P000000010/C000000001", "title")
    assert avu is not None


# def export_project_collection(self, project, collection, repository, message)

# def prepare_export(self, project, collection, repository):

# def set_collection_size(self, project_id, collection_id, open_collection, close_collection)


def test_rule_get_collection_tree():
    collection = RuleJSONManager(admin_mode=True).get_collection_tree("P000000010/C000000001")
    assert collection is not None


# def create_collection_metadata_snapshot(self, project_id, collection_id)

# def save_metadata_json_to_collection(self, project_id, collection_id, instance, schema_dict)

# def set_acl_for_metadata_snapshot(
#         self, project_id: str, collection_id: str, user: str, open_acl: str, close_acl: str
# )

# def read_schema_from_collection(self, project_id: str, collection_id: str) -> dict:
#
# def read_schema_version_from_collection(self, project_id: str, collection_id: str, version: str) -> dict:
#
# def read_instance_from_collection(self, project_id: str, collection_id: str) -> dict:
#
# def parse_general_instance(instance: dict) -> GeneralInstance:
#
# def read_instance_version_from_collection(self, project_id: str, collection_id: str, version: str) -> dict:


def test_rule_get_collection_size_per_resource():
    result = RuleManager(admin_mode=True).get_collection_size_per_resource("P000000017")
    assert result is not None


# @pytest.mark.skip(reason="needs local setup first.")
# def test_rule_get_collections_var_config():
#     config = dict()
#     config["IRODS_HOST"] = "0.0.0.0"
#     config["IRODS_USER"] = "rods"
#     config["IRODS_PASS"] = "irods"
#     result = RuleManager(config=config).get_collections("/nlmumc/projects/P000000011")
#     collections = result.collections
#     assert collections is not None
#     assert collections[0].creator == "irods_bootstrap@docker.dev"
#
#
# @pytest.mark.skip()
# def test_rule_export():
#     result = False
#     try:
#         # RuleManager(admin_mode=True).export_project_collection("P000000016", "C000000001", "DataverseNL", {})
#         RuleManager("dlinssen").export_project_collection("P000000016", "C000000001", "DataverseNL", {})
#     except CAT_NO_ACCESS_PERMISSION:
#         result = True
#
#     assert result is True
#
#
# @pytest.mark.skip()
# def test_rule_archive():
#     result = False
#     try:
#         # RuleManager("service-surfarchive").archive_project_collection("/nlmumc/projects/P000000016/C000000001")
#         RuleManager("jmelius").archive_project_collection("/nlmumc/projects/P000000015/C000000001")
#     except CAT_NO_ACCESS_PERMISSION:
#         result = True
#
#     assert result is True
#
#
# @pytest.mark.skip(reason="needs local setup first.")
# def test_publish_message():
#     message = {
#         "project": "P000000015",
#         "collection": "C000000002",
#         "repository": "Dataverse",
#         "dataverse_alias": "DataHub",
#         "restrict": False,
#         "restrict_list": "P000000015/C000000002/specialchars_~!@#$%^&()-+=[]{};',.txt,\tP000000015/C000000002/test.log",
#         "data_export": False,
#         "delete": False,
#         "depositor": "jonathan.melius@maastrichtuniversity.nl",
#     }
#     json_message = json.dumps(message)
#     publish_message("datahub.events_tx", "projectCollection.exporter.requested", json_message)
#     assert True is True
#
#
# @pytest.mark.skip(reason="needs local setup first.")
# def test_export_project_collection_by_step():
#     project = "P000000015"
#     collection = "C000000002"
#     repository = "Dataverse"
#
#     RuleManager(admin_mode=True).prepare_export(project, collection, repository)
#
#     message = {
#         "project": project,
#         "collection": collection,
#         "repository": repository,
#         "dataverse_alias": "DataHub",
#         "restrict": False,
#         "restrict_list": "P000000015/C000000002/specialchars_~!@#$%^&()-+=[]{};\"',.txt,\tP000000015/C000000002/test.log",
#         "data_export": False,
#         "delete": False,
#         "depositor": "jonathan.melius@maastrichtuniversity.nl",
#     }
#     json_message = json.dumps(message)
#     publish_message("datahub.events_tx", "projectCollection.exporter.requested", json_message)
#     assert True is True
#
#
# @pytest.mark.skip(reason="needs local setup first.")
# def test_rule_export_project_collection():
#     project = "P000000015"
#     collection = "C000000002"
#     repository = "Dataverse"
#     message = {
#         "project": project,
#         "collection": collection,
#         "repository": repository,
#         "dataverse_alias": "DataHub",
#         "restrict": False,
#         "restrict_list": "P000000015/C000000002/specialchars_~!@#$%^&()-+=[]{};\"',.txt,\tP000000015/C000000002/test.log",
#         "data_export": False,
#         "delete": False,
#         "depositor": "jonathan.melius@maastrichtuniversity.nl",
#     }
#     RuleManager(admin_mode=True).export_project_collection(project, collection, repository, message)
#
#     assert True is True
