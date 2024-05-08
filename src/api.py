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

    def LibraryContent(self, library_id, method="GET", params={}):
        params["ParentId"] = library_id
        params["Fields"] = ",".join(
            [
                ",Budget,DateCreated,Genres,People,Revenue",
                "IndexOptions,Overview,ParentId,Studios",
            ]
        )

        return self._send_request("Items", method=method, params=params)

    def Collections(self, method="POST", params=None):

        return self._send_request(
            "Collections", method=method, params=params, stripItems=False
        )

    def update_collection(self, name, ids):
        start_index = 0
        batch_counter = 1
        batch_size = 50
        total_batches = max(1, len(ids) // batch_size)

        while start_index < len(ids):
            logger.debug(f"Processing batch {batch_counter} of {total_batches}")
            end_index = min(start_index + batch_size, len(ids))
            batch = ",".join(ids[start_index:end_index])

            self._send_request(
                "Collections",
                method="POST",
                params={"Name": name, "Ids": batch},
                stripItems=False,
            )

            start_index += batch_size
            batch_counter += 1
