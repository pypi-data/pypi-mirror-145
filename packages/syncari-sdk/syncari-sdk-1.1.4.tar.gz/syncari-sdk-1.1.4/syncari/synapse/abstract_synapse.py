from abc import ABC, abstractmethod
from asyncio.log import logger
import json
from requests import Response
from syncari.models.request import (DescribeRequest, ErrorResponse,
    SyncRequest, WebhookRequest, RequestType, Request)
from syncari.rest.client import SyncariException
from ..logger import SyncariLogger

# pylint: disable=missing-function-docstring
class Synapse(ABC):
    """
        The abstract synapse class to enforce synapse implementations
    """
    raw_request = None
    connection = None
    request = None
    request_type = None

    def __init__(self, raw_request: Request) -> None:
        self.raw_request = raw_request

    def execute(self):
        """
            The route method that looks for the type of the synapse request and invokes
            appropriate synapse supported method.
        """
        self.logger.info(self.raw_request)
        response = None
        try:
            self.raw_request = Request.parse_raw(self.raw_request)
            self.connection = self.raw_request.connection
            self.request_type = self.raw_request.type

            if self.request_type == RequestType.CONNECT:
                response = self.connect()
            elif self.request_type == RequestType.SYNAPSE_INFO:
                response = self.synapse_info()
            elif self.request_type == RequestType.DESCRIBE:
                self.request = DescribeRequest.parse_obj(self.raw_request.body)
                response = self.describe()
            elif self.request_type == RequestType.READ:
                self.request = SyncRequest.parse_obj(self.raw_request.body)
                response = self.read()
            elif self.request_type == RequestType.GET:
                self.request = SyncRequest.parse_obj(self.raw_request.body)
                response = self.get()
            elif self.request_type == RequestType.CREATE:
                self.request = SyncRequest.parse_obj(self.raw_request.body)
                response = self.create()
            elif self.request_type == RequestType.UPDATE:
                self.request = SyncRequest.parse_obj(self.raw_request.body)
                response = self.update()
            elif self.request_type == RequestType.DELETE:
                self.request = SyncRequest.parse_obj(self.raw_request.body)
                response = self.delete()
            elif self.request_type == RequestType.EXTRACT_WEBHOOK_IDENTIFIER:
                self.request = WebhookRequest.parse_obj(self.raw_request.body)
                response = self.extract_webhook_identifier()
            elif self.request_type == RequestType.PROCESS_WEBHOOK:
                self.request = WebhookRequest.parse_obj(self.raw_request.body)
                response = self.process_webhook()
            else:
                self.request = SyncRequest.parse_obj(self.raw_request.body)
                response = self.read()

        except SyncariException as e:
            response = e.error_response
            
        except Exception as e:
            err_msg = 'Failed to execute request {}'.format(self.request_type)
            err = Response()
            err.status_code = 400
            err.reason = err_msg
            err.raw = str(e)
            err.url = self.connection.endpoint
            response = ErrorResponse(message=err_msg, response=err)

        if (isinstance(response, list)):
            json_vals = []
            for v in response:
                json_vals.append(v.json())
            return json.dumps(json_vals)

        try:
            json_resp = response.json()
            return json_resp
        except:
            logger.warn('Response was not serializable: {}'.format(response))
            return response

        
    @property
    def name(self) -> str:
        """
            Synapse name.
        """
        return self.__class__.__name__

    def print(self, funcname, request):
        self.logger.info(funcname)
        self.logger.info(request)
        print()

    @property
    def logger(self):
        return SyncariLogger.get_logger(f"{self.name}")

    @abstractmethod
    def synapse_info(self):
        pass

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def describe(self):
        pass

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def extract_webhook_identifier(self):
        pass

    @abstractmethod
    def process_webhook(self):
        pass
