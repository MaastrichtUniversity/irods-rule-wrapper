import pytest
import irodsrulewrapper.utils


# TODO: Is there a better, safer way?
@pytest.fixture(autouse=True)
def monkeypatch_ssl_settings():
    import pathlib

    print(pathlib.Path(__file__).parent.resolve())
    irodsrulewrapper.utils.BaseRuleManager.ssl_context.load_verify_locations(
        "/home/jonathan/DataHub/DH-env/env4/docker-dev/externals/irods-rule-wrapper/tests/test_only_dev_irods_dh_ca_cert.pem"
    )
