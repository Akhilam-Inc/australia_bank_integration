import requests
import frappe
from urllib.parse import urljoin
from enum import Enum
from frappe import _
from frappe.utils.background_jobs import enqueue
from datetime import datetime, timedelta

class SupportedHTTPMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"

class AirwallexBase:
    BASE_PATH = ""

    def __init__(self, use_auth_headers=False):
        self.airwallex_setting = frappe.get_single("Bank Integration Setting")
        self.client_id = self.airwallex_setting.client_id
        self.api_key = self.airwallex_setting.get_password("api_key")
        self.base_url = self.airwallex_setting.api_url
        self.enable_api_log = True

        # Set headers based on whether this is for authentication or API calls
        if use_auth_headers:
            # Headers for authentication endpoint
            self.headers = {
                "x-api-key": self.api_key,
                "x-client-id": self.client_id,
                "Content-Type": "application/json"
            }
            self.is_auth_instance = True
        else:
            # Headers for API calls - token will be added when making requests
            self.headers = {
                "Content-Type": "application/json"
            }
            self.is_auth_instance = False

        self.log_data = {}

    def get_valid_token(self):
        """Get a valid bearer token, authenticate if needed"""
        # Check if we have a cached token that's still valid
        cached_token = frappe.cache.get_value("airwallex_bearer_token")
        expires_at = frappe.cache.get_value("airwallex_token_expires_at")

        if cached_token and expires_at:
            # Check if token is still valid (with 5 minute buffer)
            try:
                expires_datetime = datetime.fromisoformat(expires_at.replace('Z', '+00:00'))
                if datetime.now() < expires_datetime - timedelta(minutes=5):
                    return cached_token
            except:
                pass  # If date parsing fails, get a new token

        # Token expired or doesn't exist, get a new one
        return self.authenticate_and_cache_token()

    def authenticate_and_cache_token(self):
        """Authenticate and cache the token"""
        # Import here to avoid circular import
        from bank_integration.airwallex.api.airwallex_authenticator import AirwallexAuthenticator

        auth = AirwallexAuthenticator()
        auth_response = auth.authenticate()

        if not auth_response or not auth_response.get('token'):
            frappe.throw("Failed to authenticate with Airwallex API")

        token = auth_response['token']
        expires_at = auth_response.get('expires_at')

        # Cache the token with 1 hour expiration
        try:
            frappe.cache.setex("airwallex_bearer_token", 3600, token)
            if expires_at:
                frappe.cache.setex("airwallex_token_expires_at", 3600, expires_at)
        except AttributeError:
            # Fallback if setex is not available
            frappe.cache.set_value("airwallex_bearer_token", token)
            if expires_at:
                frappe.cache.set_value("airwallex_token_expires_at", expires_at)

        return token

    def ensure_authenticated_headers(self):
        """Ensure headers have valid bearer token"""
        if "Authorization" not in self.headers:
            token = self.get_valid_token()
            self.headers["Authorization"] = f"Bearer {token}"

    def get(self, endpoint=None, params=None, headers=None):
        # Ensure we have auth token for API calls (not auth endpoints)
        if not self.is_auth_instance:
            self.ensure_authenticated_headers()
        return self._make_request(SupportedHTTPMethod.GET, endpoint=endpoint, params=params, headers=headers)

    def delete(self, endpoint=None, params=None, headers=None):
        if not self.is_auth_instance:
            self.ensure_authenticated_headers()
        return self._make_request(SupportedHTTPMethod.DELETE, endpoint=endpoint, params=params, headers=headers)

    def post(self, endpoint, params=None, json=None, headers=None):
        if not self.is_auth_instance:
            self.ensure_authenticated_headers()
        return self._make_request(SupportedHTTPMethod.POST, endpoint, params=params, json=json, headers=headers)

    def put(self, endpoint=None, json=None, headers=None):
        if not self.is_auth_instance:
            self.ensure_authenticated_headers()
        return self._make_request(SupportedHTTPMethod.PUT, endpoint=endpoint, json=json, headers=headers)

    def _make_request(self, method: SupportedHTTPMethod, endpoint=None, params=None, json=None, headers=None):
        """Base method for making HTTP requests."""
        url = self._build_url(endpoint, method)
        request_headers = {**self.headers, **(headers or {})}

        # Ensure API key is always included in params
        params = params or {}
        # params["API-Key"] = self.api_key

        self._prepare_log(url, params, json, request_headers)
        response = None

        try:
            response = requests.request(method.value, url, params=params, json=json, headers=request_headers)

            # Try to parse JSON response, fallback to text if it fails
            try:
                response_data = response.json()
            except ValueError:
                # Response is not JSON (like HTML error pages)
                response_data = response.text

            self.create_connection_log(
                status=str(response.status_code),
                message=str(response.text),
                response=response_data,
                method=method.value,  # Convert enum to string
                payload = str(params) if json is None else str(json),
                url=url  # Pass the actual URL
            )

            # Check if the request was successful
            if response.status_code >= 400:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                frappe.throw(_("Airwallex API request failed: {0}").format(error_msg))

            # Return JSON if available, otherwise return text
            return response_data if isinstance(response_data, dict) else {"error": response_data}

        except Exception as e:
            error_response = response.text if response else str(e)
            self.create_connection_log(
                status=response.status_code if response else 500,
                message="Error",
                response=error_response,
                method=method.value,  # Convert enum to string
                payload = str(params) if json is None else str(json),
                url=url  # Pass the actual URL
            )
            frappe.throw(_("Airwallex API request failed: {0}").format(str(e or "An Error occured !!").replace(self.api_key, "****")))

        finally:
            self._log_request()

    def _build_url(self, endpoint, method):
        """Generate full API URL ensuring correct formatting."""
        base_url = self.base_url+ "/"  # Ensure base_url has a trailing slash
        base_path = self.BASE_PATH  # Keep BASE_PATH as-is
        endpoint = endpoint # Remove leading slash from endpoint

        # Build full URL dynamically
        full_url = "/".join(filter(None, [base_url.rstrip("/"), base_path, endpoint]))

        return full_url


    def _prepare_log(self, url, params, json, headers):
        self.log_data = {
            "url": url,
            "params": params,
            "request_body": json,
            "headers": self._mask_sensitive_info(headers)
        }

    def _log_request(self):
        if "Shipstation Integration" not in self.log_data:
            self.log_data["integration_request_service"] = "Shipstation Integration"
        enqueue(self._enqueue_log, log_data=self.log_data)

    def _mask_sensitive_info(self, data):
        if not isinstance(data, dict):
            return data
        sensitive_fields = {"key", "password", "token", "auth", "secret"}
        return {k: "****" if any(s in k.lower() for s in sensitive_fields) else v for k, v in data.items()}

    def _enqueue_log(self, log_data):
        # Replace this with actual logging method if required
        frappe.logger().info(log_data)

    def create_connection_log(self, status, message, response=None, method=None, payload=None, url=None):
        """Create log entry for connection test"""
        try:
            status_string = "Success" if str(status).startswith("2") else "Error"
            log = frappe.get_doc({
                "doctype": "Bank Integration Log",
                "status": str(status_string),
                "message": str(message),
                "response_data": str(response) if response else "",
                "request_data": str(payload) if payload else "",
                "url": url or self.log_data.get("url", ""),  # Use passed URL or from log_data
                "method": str(method) if method else "",
                "status_code": str(status),
            })
            if self.enable_api_log:
                log.insert(ignore_permissions=True)
                return log

        except Exception as e:
            frappe.log_error(message=str(e), title="Bank Integration Log Creation Error")
            return None
