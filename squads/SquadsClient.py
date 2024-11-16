import requests
from typing import Optional


class SquadsClient:
    def __init__(self):
        self._base_url = "http://127.0.0.1:5000/api"
        self._headers = {"login": "", "password": ""}

    def get(self, path: str) -> dict:
        return requests.get(self._base_url + path, headers=self._headers).json()

    def post(self, path: str, json: dict) -> Optional[dict]:
        return requests.post(self._base_url + path, json=json, headers=self._headers).json()

    def put(self, path: str, json: dict) -> Optional[dict]:
        return requests.put(self._base_url + path, json=json, headers=self._headers).json()

    def delete(self, path: str, json: dict) -> Optional[dict]:
        return requests.delete(self._base_url + path, json=json, headers=self._headers).json()

    def setup(self, login: str, password: str) -> None:
        self._headers = {"login": login, "password": password}


client = SquadsClient()
