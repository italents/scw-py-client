import requests
import json
import os
from pydantic import validate_arguments, ValidationError

class ScalewayAPI:

    def __init__(self, name: str, version: str, region: str="fr-par"):
        token = os.getenv("SCALEWAY_API_TOKEN")
        if not token:
            raise Exception("SCALEWAY_API_TOKEN must be defined as environment variable")
        self.api_url = f"https://api.scaleway.com/{name}/{version}/regions/{region}"
        self.headers = {
            "accept": "application/json",
            "X-Auth-Token": token,
            "Content-Type": "application/json"
        }

    def request(self, url, method="GET", data={}):
        if method == "GET":
            res = requests.get(self.api_url + url, headers=self.headers, params=data)
        elif method == "POST":
            res = requests.post(self.api_url + url, headers=self.headers, data=json.dumps(data))
        elif method == "PATCH":
            res = requests.patch(self.api_url + url, headers=self.headers, data=json.dumps(data))
        elif method == "DELETE":
            res = requests.patch(self.api_url + url, headers=self.headers)
        else:
            raise Exception(f"Unhandled method: {method}")
        if not res.ok:
            print(res.text)
        res.raise_for_status()
        return json.dumps(res.json(), indent=4, sort_keys=True)
