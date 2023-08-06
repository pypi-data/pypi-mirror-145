from billing_sync.Resources.billers import Biller
from billing_sync.Resources.resource import Resource

# This the class that will be used to get the Biller object with all the Billing resources
# This class is to implement any methods related to authentication with nash developer identity
# Or if you want to set global restrictions accross all resources
class Nash(Resource):

    _headers = {
        'Content-Type': 'application/json'
    }

    _params = {}

    _response = {}

    _is_logged_in = False

    _biller = None

    _access_token = None

    _user_id = -1

    def __init__(self):
        super().__init__("NashAPI", self._headers, self._params)

    def login(self, payload=None, method='POST', endpoint="/auth/login"):
        # authenticate and provide user credentials
        # set response here

        self._is_logged_in = True

        return self

    def sign_up(self, payload=None, method='POST', endpoint="/users", log_in_user=True):
        # authenticate and provide user credentials
        # set response here

        self.login(payload={"username": payload.get(
                    "username"), "password": payload.get("password")}).response()

        return self

    # Method used to access the Biller object with all the Billing resources
    # A singleton design is used to ensure that this object is only called once
    def biller(self, biller_id=0):

        if self._biller is None:
            self._biller = Biller(self, biller_id)

        return self._biller

    # def user(self):
    #     return Users(self)

    def is_logged_in(self):
        return self._is_logged_in

    def _set_access_token(self, access_token):
        self._access_token = access_token
        return self

    def get_access_token(self):
        return self._access_token
