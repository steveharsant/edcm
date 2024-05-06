import requests
from loguru import logger


class api:

    def __init__(self, base_url, api_token) -> None:
        self.base_url = f"{base_url}/emby"
        self.auth_string = f"api_key={api_token}"

    def _send_request(self, endpoint, method="GET", params=None, stripItems=True):
        endpoint_url = f"{self.base_url}/{endpoint}?{self.auth_string}"
        response = requests.request(method, endpoint_url, params=params)

        if response.status_code == 200:
            return response.json()["Items"] if stripItems is True else response.json()
        else:
            logger.error(f"Received {response.status_code} from endpoint {endpoint}")

    def Items(self, method="GET", params=None):
        return self._send_request("Items", method=method, params=params)

    def Libraries(self, method="GET", params=None):
        return self._send_request("Library/MediaFolders", method=method, params=params)

    def Collections(self, method="POST", params=None):
        return self._send_request(
            "Collections", method=method, params=params, stripItems=False
        )
