import pytest

from dhpythonirodsutils import validators
from dhpythonirodsutils.exceptions import ValidationError

from irodsrulewrapper.utils import convert_to_current_timezone


@pytest.mark.parametrize(
    "date, expected_result",
    [
        ("2026-01-15 12:00:00", "2026-01-15 13:00:00"),
        ("2026-07-15 12:00:00", "2026-07-15 14:00:00"),
    ],
)
def test_convert_to_current_timezone(date, expected_result):
    assert convert_to_current_timezone(date) == expected_result


@pytest.mark.parametrize(
    "path, expected_result",
    [
        ("/nlmumc/projects/P000000001/C000000001/bla/blabla/tx.txt", True),
        ("/nlmumc/projects/P000000001/C000000001/blab/../../../../blob/tx.txt", False),
        ("/nlmumc/projects/P000000001/C000000001/blab/../../../blob/tx.txt", False),
        ("/nlmumc/projects/P000000001/C000000001/blab/../../blob/tx.txt", False),
        ("/nlmumc/projects/P000000001/C000000001/blab/../blob/tx.txt", True),
    ],
)
def test_is_safe_path(path, expected_result):
    basedir = "/nlmumc/projects/P000000001/C000000001"
    result = True
    try:
        validators.validate_path_safety(basedir, path)
    except ValidationError:
        result = False
    assert result is expected_result
