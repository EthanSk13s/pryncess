import json
import requests

from typing import Any

class Client:
    def __init__(self, request_session: requests.Session | bool = True, timeout:int = 10):
        self.path = f"https://api.matsurihi.me/api"
        self.timeout = timeout
        self.retries = 5

        if isinstance(request_session, requests.Session):
            self._session = request_session
        else:
            if request_session:
                self._session = requests.Session()
            else:
                from requests import api
                self._session = api

    # This function is based off pyKirara so it's mostly the same
    def _internal_call(self, method: str, url: str, payload: Any | None, params) -> Any | bytes | None:
        args = dict(params=params)
        args['timeout'] = self.timeout
        args['params']['prettyPrint'] = False

        if payload:
            args['data'] = json.dumps(payload)

        r = self._session.request(method, url, **args)
        if r.status_code == 400 or r.status_code in [401, 402, 502]:
            return None
        
        if r.headers['content-type'] == 'application/json; charset=utf-8':
            try:
                result = r.json()

                return result
            except requests.exceptions.JSONDecodeError as e:
                raise e

        elif r.headers['content-type'] == 'image/png':

            return r.content

    def get(self, url: str, args=None, payload: Any | None = None, **kwargs) -> Any | bytes | None:
        if args:
            kwargs.update(args)

        reconnect = self.timeout
        while reconnect > 0:
            try:
                return self._internal_call('GET', self.path + url, payload, kwargs)
            except requests.HTTPError as e:
                raise Exception(e)