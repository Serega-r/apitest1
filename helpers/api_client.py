import requests


class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()

    def post(self, endpoint: str, data: dict = None, json: dict = None, files=None):
        return self.session.post(f"{self.base_url}{endpoint}", data=data, json=json, files=files)

    def get(self, endpoint: str, params: dict = None, headers: dict = None):
        return self.session.get(f"{self.base_url}{endpoint}", params=params, headers=headers)

    def put(self, endpoint: str, json: dict = None):
        return self.session.put(f"{self.base_url}{endpoint}", json=json)

    def delete(self, endpoint: str):
        return self.session.delete(f"{self.base_url}{endpoint}")