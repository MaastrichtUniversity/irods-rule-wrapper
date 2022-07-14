import pytest
import irodsrulewrapper.utils
import os

# TODO: Is there a better, safer way?
@pytest.fixture(autouse=True)
def monkeypatch_ssl_settings():
    import pathlib

    tests_folder = pathlib.Path(__file__).parent.resolve()
    irodsrulewrapper.utils.BaseRuleManager.ssl_context.load_verify_locations(os.path.join(tests_folder, "test_only_dev_irods_dh_ca_cert.pem"))
