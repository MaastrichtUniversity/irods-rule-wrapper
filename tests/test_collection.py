from irodsrulewrapper.dto.collection import Collection
from irodsrulewrapper.dto.collections import Collections

COLLECTION_JSON = '''
PLACEHOLDER
'''

COLLECTIONS_JSON = '''
PLACEHOLDER
'''


def test_collection():
    collection = Collection()
    assert collection is not None


def test_collections():
    collections = Collections()
    assert collections is not None