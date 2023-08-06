
from identity_sync.Resources.operations import Operations
from identity_sync.APIs.api_format import API
import json
from identity_sync.APIs.utils.generate_code import get_code


class Resource(API,Operations):

    _identity_id = None

    _operation = 0

    _user_id = None

    _response = {}

    _read_url = ""

    _api = None

    _resource_id = -1

    def set_operation(self, operation):
        self._operation = operation
        return self

    def set_identity_id(self, identity_id):
        self._identity_id = identity_id
        return self

    def set_user_id(self, user_id):
        self._user_id = user_id
        return self

    def set_urls(self, urls):
        self.set_read_url(urls.get("read", ""))
        return self

    def read(self, payload=None, params=''):
        # Check if the biller exists
        if self.get_identity_id() in self.KYC_CONF.keys():
            # set KYC_IDENTITIES to be the default operation when no operation is passed
            # get a billler's API details
            biller = self.KYC_CONF.get(self.get_identity_id(), self.KYC_IDENTITIES)

            endpoint = biller.get('read', {}).get('endpoint', '')

            operation, method = biller.get('read', {}).get(
                'operations', {}).get(self.get_operation(), self.KYC_IDENTITIES)

            # Check if any query params where passed, while creating the end point
            if bool(params):
                endpoint = f'{endpoint}/{operation}?{params}'
            else:
                endpoint = f'{endpoint}/{operation}'

            super().set_full_url(full_url=f"{biller.get('url','')}/{endpoint}")

            # Call the method exec to make the request to A.P.I. endpoint and return the data that will be returned in this method
            self._response = self._exec(payload, method)

        else:
            self._response = {'error':'Biller ID Does not Exist'}
        return self

    def payload(self):
        return {}

    def serialize(self):
        return self

    def response(self):
        return self._response

    def set_response(self, response={}):
        self._response = response
        return self

    def set_read_url(self, read_url):
        self._read_url = read_url
        return self

    def get_read_url(self):
        return self._read_url

    def get_identity_id(self):
        return self._identity_id

    def get_user_id(self):
        return self._user_id

    def generate_code(self, length=6):
        return get_code(length)

    def get_operation(self):
        return self._operation

    # This is the method that will be called execute an A.P.I. request.
    # Since most of the A.P.I. calls methods are similar, they are to be placed inside this method to avoid code duplication.
    #
    # It will only accept parameters unique to each A.P.I. request.
    def _exec(self, payload=None, method='POST', files=None):

        if files is None:
            payload = json.dumps(payload)
        else:
            payload = payload

        # Call the A.P.I. url by passing the variables to the super class method responsible for making requests to A.P.I. endpoints
        # The super class method returns a response that is returned by this method
        return super().api_request(payload=payload, method=method, files=files)