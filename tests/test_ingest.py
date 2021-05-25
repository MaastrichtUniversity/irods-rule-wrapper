from irodsrulewrapper.rule import RuleManager
from irodsrulewrapper.dto.metadata_xml import MetadataXML
import pytest

'''
These tests need a specific setup.
Comment out the @pytest.mark.skip to trigger these tests
Make the you set the variables according to your local setup.
'''


@pytest.mark.skip(reason='excluded from overall testing because these need specific setup.')
def test_rule_create_ingest():
    result = RuleManager().create_ingest('jmelius', 'token1', 'P000000014', 'Title1')
    assert result is None


@pytest.mark.skip(reason='excluded from overall testing because these need specific setup.')
def test_rule_create_drop_zone():
    data = {
        "user": 'jmelius',
        "creator": 'jmelius',
        "project": 'P000000016',
        "title": 'Title0',
        "date": '2021-02-26',
        "articles": '10.1016/j.cell.2021.02.021,10.1126/science.abc4346'
    }
    token = RuleManager().create_drop_zone(data)
    print(token)
    assert token is not None


@pytest.mark.skip(reason='excluded from overall testing because these need specific setup.')
def test_write_metadata_xml():
    data = {
        "user": 'jmelius', "creator": 'jmelius',
        "project": 'P000000017', "title": 'Title0', "description": 'description',
        "date": '2021-02-26', "token": 'Title0',
        "articles": '10.1016/j.cell.2021.02.021,10.1126/science.abc4346',
        "organism_id": "ncbitaxon:http://purl.obolibrary.org/obo/NCBITaxon_9606",
        "organism_label": "Homo sapiens",
        "tissue_id": "efo:http://www.ebi.ac.uk/efo/EFO_0000803",
        "tissue_label": "renal system",
        "technology_id": "ero:http://purl.obolibrary.org/obo/ERO_0000570",
        "technology_label": "heart perfusion",
        "factors": ["heart perfusion", "test1"]
    }
    rule_manager = RuleManager()
    xml = MetadataXML.create_from_dict(data)
    xml.write_metadata_xml(rule_manager.session)
    assert xml is not None


@pytest.mark.skip(reason='excluded from overall testing because these need specific setup.')
def test_read_metadata_xml_dropzone():
    token = "glorious-caterpillar"
    xml = RuleManager().read_metadata_xml(token=token)
    assert xml is not None


@pytest.mark.skip(reason='excluded from overall testing because these need specific setup.')
def test_read_metadata_xml_collection():
    xml = RuleManager().read_metadata_xml(project_id='P123456789', collection_id='C123456789')
    assert xml is not None


@pytest.mark.skip(reason='excluded from overall testing because these need specific setup.')
def test_read_metadata_xml_invalid():
    with pytest.raises(ValueError, match=r'.*missing keyword.*'):
        RuleManager().read_metadata_xml(my_var='THIS WILL GENERATE AN ERROR')


@pytest.mark.skip(reason='excluded from overall testing because these need specific setup.')
def test_rule_start_ingest():
    result = RuleManager().start_ingest('jmelius', 'token')
    assert result is None
