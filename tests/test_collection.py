from irodsrulewrapper.dto.collection import Collection
from irodsrulewrapper.dto.collections import Collections
from irodsrulewrapper.rule import RuleManager
import json

COLLECTION_JSON = '''
PLACEHOLDER
'''

COLLECTIONS_JSON = '''
PLACEHOLDER
'''


def test_rule_get_collections():
    result = RuleManager().get_collections("/nlmumc/projects/P000000010")
    collections = result.collections
    assert collections is not None


def test_collection():
    collection = Collection()
    assert collection is not None


def test_collections():
    collections = Collections()
    assert collections is not None
