# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import pytest
from azure.iot.device.iothub.pipeline import constant

"""---Constants---"""

shared_access_key = "Zm9vYmFy"
# shared_access_key_name = "alohomora" # do we need this?
hostname = "beauxbatons.academy-net"
device_id = "MyPensieve"
module_id = "Divination"
gateway_hostname = "EnchantedCeiling"
signature = "IsolemnlySwearThatIamuUptoNogood"  # does this need to be something else?
expiry = "1539043658"


"""----Shared connection string fixtures """

device_connection_string_format = (
    "HostName={hostname};DeviceId={device_id};SharedAccessKey={shared_access_key}"
)
device_connection_string_gateway_format = "HostName={hostname};DeviceId={device_id};SharedAccessKey={shared_access_key};GatewayHostName={gateway_hostname}"

module_connection_string_format = "HostName={hostname};DeviceId={device_id};ModuleId={module_id};SharedAccessKey={shared_access_key}"
module_connection_string_gateway_format = "HostName={hostname};DeviceId={device_id};ModuleId={module_id};SharedAccessKey={shared_access_key};GatewayHostName={gateway_hostname}"


@pytest.fixture(params=["Device Connection String", "Device Connection String w/ Protocol Gateway"])
def device_connection_string(request):
    string_type = request.param
    if string_type == "Device Connection String":
        return device_connection_string_format.format(
            hostname=hostname, device_id=device_id, shared_access_key=shared_access_key
        )
    else:
        return device_connection_string_gateway_format.format(
            hostname=hostname,
            device_id=device_id,
            shared_access_key=shared_access_key,
            gateway_hostname=gateway_hostname,
        )


@pytest.fixture(params=["Module Connection String", "Module Connection String w/ Protocol Gateway"])
def module_connection_string(request):
    string_type = request.param
    if string_type == "Module Connection String":
        return module_connection_string_format.format(
            hostname=hostname,
            device_id=device_id,
            module_id=module_id,
            shared_access_key=shared_access_key,
        )
    else:
        return module_connection_string_gateway_format.format(
            hostname=hostname,
            device_id=device_id,
            module_id=module_id,
            shared_access_key=shared_access_key,
            gateway_hostname=gateway_hostname,
        )


"""----Shared sas token fixtures---"""

sas_token_format = "SharedAccessSignature sr={uri}&sig={signature}&se={expiry}"
# when to use the skn format?
sas_token_skn_format = (
    "SharedAccessSignature sr={uri}&sig={signature}&se={expiry}&skn={shared_access_key_name}"
)

# what about variant input with different ordered attributes
# SharedAccessSignature sig={signature-string}&se={expiry}&skn={policyName}&sr={URL-encoded-resourceURI}


@pytest.fixture()
def device_sas_token_string():
    uri = hostname + "/devices/" + device_id
    return sas_token_format.format(uri=uri, signature=signature, expiry=expiry)


@pytest.fixture()
def module_sas_token_string():
    uri = hostname + "/devices/" + device_id + "/modules/" + module_id
    return sas_token_format.format(uri=uri, signature=signature, expiry=expiry)


"""----Shared Edge Container configuration---"""

fake_ca_cert = "__FAKE_CA_CERTIFICATE__"
fake_digest = "__FAKE_DIGEST__"


@pytest.fixture()
def edge_container_env_vars():
    return {
        "IOTEDGE_MODULEID": "__FAKE_MODULE_ID__",
        "IOTEDGE_DEVICEID": "__FAKE_DEVICE_ID__",
        "IOTEDGE_IOTHUBHOSTNAME": "__FAKE_HOSTNAME__",
        "IOTEDGE_GATEWAYHOSTNAME": "__FAKE_GATEWAY_HOSTNAME__",
        "IOTEDGE_APIVERSION": "__FAKE_API_VERSION__",
        "IOTEDGE_MODULEGENERATIONID": "__FAKE_MODULE_GENERATION_ID__",
        "IOTEDGE_WORKLOADURI": "http://__FAKE_WORKLOAD_URI__/",
    }


"""----Shared mock pipeline adapter fixture----"""


class FakePipelineAdapter:
    def __init__(self):
        self.feature_enabled = {}  # This just has to be here for the spec

    def connect(self, callback=None):
        callback()

    def disconnect(self, callback=None):
        callback()

    def enable_feature(self, feature_name, callback=None):
        callback()

    def disable_feature(self, feature_name, callback=None):
        callback()

    def send_event(self, event, callback=None):
        callback()

    def send_output_event(self, event, callback=None):
        callback()

    def send_method_response(self, method_response, callback=None):
        callback()


@pytest.fixture
def pipeline(mocker):
    """This fixture will automatically handle callbacks and should be
    used in the majority of tests.
    """
    return mocker.MagicMock(wraps=FakePipelineAdapter())


@pytest.fixture
def pipeline_manual_cb(mocker):
    """This fixture is for use in tests where manual triggering of a
    callback is required
    """
    return mocker.MagicMock()