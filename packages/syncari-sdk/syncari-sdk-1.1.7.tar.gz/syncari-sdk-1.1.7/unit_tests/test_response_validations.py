
# pylint: disable=missing-class-docstring, import-error, missing-function-docstring
import json
from syncari.models.core import (AuthConfig, Connection, AuthType, 
    AuthField, AuthMetadata, UIMetadata, SynapseInfo, Record, Result,EventData,WebhookOperation)
from syncari.models.request import (DescribeRequest, ErrorResponse,
    Request, SyncRequest, Watermark, WebhookRequest, RequestType, ReadResponse)
from syncari.models.schema import Schema, Attribute

from syncari.synapse.abstract_synapse import Synapse

class MockResponseValidationSynapse(Synapse):

    def __print(self, funcname, request):
        self.logger.info(funcname)
        self.logger.info(request)
        print()

    def connect(self):
        connections = []
        connections.append(self.connection)
        return connections

    def synapse_info(self):
        return []

    def describe(self):
        self.__print(self.describe.__name__, self.request)
        return Schema.parse_obj({'apiName':'MockSchema','displayName':'MockDisplayName'})

    def read(self):
        self.__print(self.read.__name__, self.request)
        watermark = self.request.watermark
        return Record.parse_obj({'name':'MockRecord','values':{'key':'val'}})

    def get(self):
        self.__print(self.get.__name__, self.request)
        return Record.parse_obj({'name':'MockRecord','values':{'key':'val'}})

    def create(self):
        self.__print(self.create.__name__, self.request)
        return Result.parse_obj({'id':'MockID'})

    def update(self):
        self.__print(self.update.__name__, self.request)
        return Result.parse_obj({'id':'MockID'})

    def delete(self):
        self.__print(self.delete.__name__, self.request)
        return Result.parse_obj({'id':'MockID'})

    def extract_webhook_identifier(self):
        self.__print(self.extract_webhook_identifier.__name__, self.request)
        return ['MockWebhookID']

    def process_webhook(self):
        self.__print(self.process_webhook.__name__, self.request)
        return Result.parse_obj({'id':'MockID'})

def test_connect():
    synapse_request = Request(type=RequestType.CONNECT,
        connection=get_connection(),
        body=None).json()
    synapse = MockResponseValidationSynapse(synapse_request)
    resp = synapse.execute()
    assert resp is not None
    assert isinstance(resp, ErrorResponse)
    assert resp.response.reason == 'Invalid response type for request RequestType.CONNECT'

def test_get_synapse_info():
    synapse_request = Request(type=RequestType.SYNAPSE_INFO,
        connection=get_connection(),
        body=None).json()
    synapse = MockResponseValidationSynapse(synapse_request)
    resp = synapse.execute()
    assert resp is not None
    assert isinstance(resp, ErrorResponse)
    assert resp.response.reason == 'Invalid response type for request RequestType.SYNAPSE_INFO'

def test_describe_route():
    synapse_request = Request(type=RequestType.DESCRIBE,
        connection=get_connection(),
        body=DescribeRequest(entities=['test'])).json()
    synapse = MockResponseValidationSynapse(synapse_request)
    resp = synapse.execute()
    assert resp is not None
    assert isinstance(resp, ErrorResponse)
    assert resp.message == 'Failed to execute request RequestType.DESCRIBE'
    assert resp.response.reason == '1 validation error for Schema\nattributes\n  field required (type=value_error.missing)'

def test_read_synapse_request():
    synapse_request = Request(type=RequestType.READ,
        connection=get_connection(),
        body=SyncRequest(
            entity=Schema(apiName='test',displayName='Test',attributes=[]), 
            watermark=Watermark(start=0, end=0))).json()
    synapse = MockResponseValidationSynapse(synapse_request)
    resp = synapse.execute()
    assert resp is not None
    assert isinstance(resp, ErrorResponse)
    assert resp.response.reason == 'Invalid response type for request RequestType.READ'

def test_get_synapse_request():
    synapse_request = Request(type=RequestType.GET,
        connection=get_connection(),
        body=SyncRequest(
            entity=Schema(apiName='test',displayName='Test',attributes=[]), 
            watermark=Watermark(start=0, end=0))).json()
    synapse = MockResponseValidationSynapse(synapse_request)
    resp = synapse.execute()
    assert resp is not None
    assert isinstance(resp, ErrorResponse)
    assert resp.response.reason == 'Invalid response type for request RequestType.GET'

def test_create_synapse_request():
    synapse_request = Request(type=RequestType.CREATE,
        connection=get_connection(),
        body=SyncRequest(
            entity=Schema(apiName='test',displayName='Test',attributes=[]), 
            watermark=Watermark(start=0, end=0))).json()
    synapse = MockResponseValidationSynapse(synapse_request)
    resp = synapse.execute()
    assert resp is not None
    assert isinstance(resp, ErrorResponse)
    assert resp.response.reason == 'Invalid response type for request RequestType.CREATE'

def test_update_synapse_request():
    synapse_request = Request(type=RequestType.UPDATE,
        connection=get_connection(),
        body=SyncRequest(
            entity=Schema(apiName='test',displayName='Test',attributes=[]), 
            watermark=Watermark(start=0, end=0))).json()
    synapse = MockResponseValidationSynapse(synapse_request)
    resp = synapse.execute()
    assert resp is not None
    assert isinstance(resp, ErrorResponse)
    assert resp.response.reason == 'Invalid response type for request RequestType.UPDATE'

def test_delete_synapse_request():
    synapse_request = Request(type=RequestType.DELETE,
        connection=get_connection(),
        body=SyncRequest(
            entity=Schema(apiName='test',displayName='Test',attributes=[]), 
            watermark=Watermark(start=0, end=0))).json()
    synapse = MockResponseValidationSynapse(synapse_request)
    resp = synapse.execute()
    assert resp is not None
    assert isinstance(resp, ErrorResponse)
    assert resp.response.reason == 'Invalid response type for request RequestType.DELETE'

def test_process_webook_request():
    synapse_request = Request(type=RequestType.PROCESS_WEBHOOK,
        connection=get_connection(),
        body=WebhookRequest(body=json.dumps([{'key':'value'}]))).json()
    synapse = MockResponseValidationSynapse(synapse_request)
    resp = synapse.execute()
    assert resp is not None
    assert isinstance(resp, ErrorResponse)
    assert resp.response.reason == 'Invalid response type for request RequestType.PROCESS_WEBHOOK'


def test_extract_webhook_identifier():
    synapse_request = Request(type=RequestType.EXTRACT_WEBHOOK_IDENTIFIER,
        connection=get_connection(),
        body=WebhookRequest(body=json.dumps([{'key':'value'}]))).json()
    synapse = MockResponseValidationSynapse(synapse_request)
    resp = synapse.execute()
    assert resp is not None
    assert isinstance(resp, ErrorResponse)
    assert resp.response.reason == 'Invalid response type for request RequestType.EXTRACT_WEBHOOK_IDENTIFIER'

def get_connection():
    authConfig=AuthConfig(endpoint='http://endpoint.com')
    connection = Connection(id='1', name='name', authConfig=authConfig, idFieldName='idfield', watermarkFieldName='watermarkfield', 
        endpoint='http://endpoint.com', createdAtFieldName='createdfield', updatedAtFieldName='updatedfield', oAuthRedirectUrl='http://redirect.com')
    return connection
