from irodsrulewrapper.rule import RuleManager


def test_rule_create_ingest():
    result = RuleManager().create_ingest('jmelius', 'token1', 'P000000014', 'Title1')
    assert result is None


def test_rule_create_drop_zone():
    data = {"user": 'jmelius', "project": 'P000000014', "title": 'TitleX', "date": '2021-02-26'}
    result = RuleManager().create_drop_zone(data)
    assert result is None

