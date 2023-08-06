
from billing_sync.APIs.api_format import API
import json
from billing_sync.APIs.utils.generate_code import get_code


class Resource(API):

    _biller_id = None

    _operation = 0

    _user_id = None

    _response = {}

    _read_url = ""

    _api = None

    _resource_id = -1

    GLOBAL = 0
    IPAY = 1
    FLUTTERWAVE = 2
    TINGG = 3

    @property
    def READ(self):
        return 0

    # These are the operations to be performed in Billing Identity
    # Each with a unique incremental ID

    # Returns Sample Data
    SAMPLE_DATA = -1
    # Returns a list of supported billers by Nash
    BILLERS = SAMPLE_DATA + 1
    # Returns a list of supported billers by Nash
    SUPPORTED_BILLERS = BILLERS + 1
    # Returns the balance in the configured billing account
    BALANCE = SUPPORTED_BILLERS + 1
    # Checks if the biller's connection/network is up/down
    BILLER_STATUS = BALANCE + 1
    # Returns the network provider using a mobile number's prefix
    NUMBER_LOOK_UP = BILLER_STATUS + 1
    # Returns the status of a transaction
    TRANSACTION_STATUS = NUMBER_LOOK_UP + 1
    # Executes a bill payment
    BILL_PAYMENT = TRANSACTION_STATUS + 1
    # Returns the bills filtered by country
    BILL_BY_COUNTRY = BILL_PAYMENT + 1
    # Returns the bills filtered by provider
    BILL_BY_PROVIDER = BILL_BY_COUNTRY + 1
    # Confirms if a client's/customer's blling account is valid
    VALIDATE_CUSTOMER = BILL_BY_PROVIDER + 1
    # Returns a generated OTP
    GENERATE_OTP = VALIDATE_CUSTOMER + 1
    # Validates a generated OTP
    VALIDATE_OTP = GENERATE_OTP + 1
    # Queries a bill
    QUERY_BILL = VALIDATE_OTP + 1

    def set_operation(self, operation):
        self._operation = operation
        return self

    def set_biller_id(self, biller_id):
        self._biller_id = biller_id
        return self

    def set_user_id(self, user_id):
        self._user_id = user_id
        return self

    def set_urls(self, urls):
        self.set_read_url(urls.get("read", ""))
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

    def get_biller_id(self):
        return self._biller_id

    def get_user_id(self):
        return self._user_id

    def generate_code(self, length=6):
        return get_code(length)

    def get_operation(self):
        return self._operation

    # All end points are placed in the BILLERS_CONF 
    # This is to allow easy standardization of the base url, endpoint and operations
    # When calling the APIs, in this case this is done in the read function
    BILLERS_CONF = {
        GLOBAL: {
            "url": "http://127.0.0.1:8000",
            "read": {
                "endpoint": f"api/billing",
                "operations": {
                    SAMPLE_DATA: ("sample_payload", "POST"),
                    BILLERS: ("billers", "GET"),
                }
            }

        },
        IPAY: {
            "url": "http://127.0.0.1:8000",
            "read": {
                "endpoint": f"api/billing/{IPAY}",
                "operations": {
                    SUPPORTED_BILLERS: ("get_billers", "GET"),
                    BILLER_STATUS: ("get_biller_status", "POST"),
                    NUMBER_LOOK_UP: ("get_number_look_up", "POST"),
                    BALANCE: ("get_account_balance", "POST"),
                    VALIDATE_CUSTOMER: ("validate_bill_account", "POST"),
                    BILL_PAYMENT: ("make_bill_payment", "POST"),
                    TRANSACTION_STATUS: ("get_transaction_status", "POST"),
                }
            }

        },
        TINGG: {
            "url": "https://dev.billingservices.nashglobal.co",
            "read": {
                "endpoint": "api/Tingg",
                "operations": {
                    BILL_PAYMENT: ("create_bill", "POST"),
                    QUERY_BILL: ("query_bill", "POST"),
                    TRANSACTION_STATUS: ("get_transaction_status", "POST"),
                }
            }

        },
        FLUTTERWAVE: {
            "url": "https://dev.billingservices.nashglobal.co",
            "read": {
                "endpoint": "api/Flutterwave",
                "operations": {
                    BILL_BY_COUNTRY: ("get_bills_by_country", "GET"),
                    BILL_BY_PROVIDER: ("get_bills_by_provider", "GET"),
                    BILL_PAYMENT: ("create_bill", "POST"),
                    VALIDATE_CUSTOMER: ("validate_customer_details", "GET"),
                    TRANSACTION_STATUS: ("get_transaction_status", "GET"),
                    GENERATE_OTP: ("generate_otp", "POST"),
                    VALIDATE_OTP: ("validate_otp", "POST"),
                }
            }

        }
    }

    def read(self, payload=None, params=''):
        # Check if the biller exists
        if self.get_biller_id() in self.BILLERS_CONF.keys():
            # set BILLERS to be the default operation when no operation is passed
            # get a billler's API details
            biller = self.BILLERS_CONF.get(self.get_biller_id(), self.BILLERS)

            endpoint = biller.get('read', {}).get('endpoint', '')

            operation, method = biller.get('read', {}).get(
                'operations', {}).get(self.get_operation(), self.BILLERS)

            # Check if any query params where passed, while creating the end point
            if bool(params):
                endpoint = f'{endpoint}/{operation}?{params}'
            else:
                endpoint = f'{endpoint}/{operation}'

            super().set_full_url(full_url=f"{biller.get('url','')}/{endpoint}")

            # Call the method exec to make the request to A.P.I. endpoint and return the data that will be returned in this method
            self._response = self._exec(payload, method, endpoint)

        else:
            self._response = {'error':'Biller ID Does not Exist'}
        return self

    # This is the method that will be called execute an A.P.I. request.
    # Since most of the A.P.I. calls methods are similar, they are to be placed inside this method to avoid code duplication.
    #
    # It will only accept parameters unique to each A.P.I. request.
    def _exec(self, payload=None, method='POST', endpoint="", files=None):

        # NCBA send data back to our callback as XML converted to bytes
        if isinstance(payload, bytes):
            payload = payload.decode("utf-8")

        if files is None:
            payload = json.dumps(payload)
        else:
            payload = payload

        # Call the A.P.I. url by passing the variables to the super class method responsible for making requests to A.P.I. endpoints
        # The super class method returns a response that is returned by this method
        return super().api_request(payload=payload, method=method, files=files)
