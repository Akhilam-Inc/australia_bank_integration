from bank_integration.airwallex.api.base_api import AirwallexBase
import frappe


class AirwallexAuthenticator(AirwallexBase):

    def __init__(self):
        # This is the key fix - pass use_auth_headers=True
        super().__init__(use_auth_headers=True)

    def authenticate(self):
        # This method will now use API key headers instead of bearer token
        return self.post(endpoint='authentication/login', json={})
