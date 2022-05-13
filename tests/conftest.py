import pytest
import irodsrulewrapper.utils

# TODO: Is there a better, safer way?
@pytest.fixture(autouse=True)
def monkeypatch_ssl_settings():
    irodsrulewrapper.utils.BaseRuleManager.ssl_context.load_verify_locations("./test_only_dev_irods_dh_ca_cert.pem")
