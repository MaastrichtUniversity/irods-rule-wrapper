from irodsrulewrapper.rule import RuleManager


# def test_rule_create_ingest():
#     result = RuleManager().create_ingest('jmelius', 'token1', 'P000000014', 'Title1')
#     assert result is None


# def test_rule_create_drop_zone():
#     data = {"user": 'jmelius', "creator": 'jmelius', "project": 'P000000017', "title": 'Title0', "date": '2021-02-26'}
#     token = RuleManager().create_drop_zone(data)
#     assert token is not None


# def test_read_metadata_xml():
#     token = "adventurous-armadillo"
#     xml = RuleManager().read_metadata_xml(token)
#     assert xml is not None


# def test_rule_start_ingest():
#     result = RuleManager().start_ingest('jmelius', 'token')
#     assert result is None
