import requests

from typing import cast

from pryncess.internals import Client
from pryncess.models.lounges import Lounge
from pryncess.types.lounges import LoungeDict


class LoungeAPI:
    def __init__(self, version: str, session: requests.Session):
        self.prefix_url =  f"/mltd/v2/{version}/lounges" 
        self._client = Client(session)
    
    def get_lounge(self, lounge: str | Lounge) -> Lounge | None:
        resp = self._client.get(f"{self.prefix_url}/{str(lounge)}")

        if not resp:
            return None
        
        cast_lounge = cast(LoungeDict, resp)

        return Lounge(cast_lounge)
    
    def search_lounge(self, name: str) -> list[Lounge] | None:
        args = {"name": name}
        resp = self._client.get(f"{self.prefix_url}", args=args)

        if not resp:
            return None
        
        if isinstance(resp, list):
            results = [Lounge(lounge) for lounge in resp]

            return results