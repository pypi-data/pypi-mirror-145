import sys

import requests
from requests.exceptions import ConnectionError


class Client:
    def __init__(self, user_id, endpoint):
        self.endpoint = endpoint if endpoint else "https://push.learningman.top"
        self.user_id = user_id

    @staticmethod
    def create(user_id, endpoint=None):
        client = Client(user_id, endpoint)
        client.check()
        return client

    def check(self):
        resp = requests.get(f"{self.endpoint}/{self.user_id}/check")
        if not resp.json():
            raise Exception("User ID not valid")

    def send(self, content, title=None, long=None):
        if content is None or content == "":
            raise Exception("Content is required")

        params = {}
        if 'unittest' in sys.modules:
            params['dry'] = True

        if title is None:
            title = "Notification"
        if long is None:
            long = ""

        data = {
            "title": title,
            "content": content,
            "long": long
        }
        try:
            resp = requests.post(f"{self.endpoint}/{self.user_id}/send", data=data, params=params)
        except ConnectionError as e:
            raise Exception("Connection error") from e
        return resp.json()
