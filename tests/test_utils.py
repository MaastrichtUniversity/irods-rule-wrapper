import pytest

from irodsrulewrapper.utils import is_safe_path


@pytest.mark.parametrize("path, expected_result", [
    ("/nlmumc/projects/P000000001/C000000001/bla/blabla/tx.txt", True),
    ("/nlmumc/projects/P000000001/C000000001/blab/../../../../blob/tx.txt", False),
    ("/nlmumc/projects/P000000001/C000000001/blab/../../../blob/tx.txt", False),
    ("/nlmumc/projects/P000000001/C000000001/blab/../../blob/tx.txt", False),
    ("/nlmumc/projects/P000000001/C000000001/blab/../blob/tx.txt", True)
    ])
def test_is_safe_path(path, expected_result):
    basedir = "/nlmumc/projects/P000000001/C000000001"
    test = is_safe_path(basedir, path)
    assert test is expected_result
