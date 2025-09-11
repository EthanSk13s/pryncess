import requests

from pryncess.internals import Client
from pryncess.models.events import Event
from pryncess.mltd.params import EventParams


class EventAPI:
    def __init__(self, version: str, session: requests.Session):
        self.prefix_url = f"/mltd/v2/{version}/events"
        self._client = Client(session)
    
    def get_events(self, params: EventParams,  event_id: int | None = None ) -> list[Event] | None:
        if event_id:
            resp = self._client.get(f"{self.prefix_url}/{event_id}", args=params.to_dict())
        else:
            resp = self._client.get(f"{self.prefix_url}/", args=params.to_dict())
        
        if resp is None:
            return None

        if isinstance(resp, list):
            events: list[Event] = [Event(card) for card in resp]
            
            return events