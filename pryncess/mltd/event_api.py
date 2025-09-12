import requests

from datetime import datetime
from typing import cast

from pryncess.internals import Client
from pryncess.models.idols import Idol
from pryncess.models.events import Event, EventBorders, EventSumm, EventLog
from pryncess.mltd.params import EventParams
from pryncess.types.events import EventBordersDict


class EventAPI:
    def __init__(self, version: str, session: requests.Session):
        self.prefix_url = f"/mltd/v2/{version}/events"
        self._client = Client(session)
    
    def get_events(
            self, params: EventParams,
            event_id: int | None = None) -> list[Event] | None:

        if event_id:
            resp = self._client.get(f"{self.prefix_url}/{event_id}",
                                    args=params.to_dict())
        else:
            resp = self._client.get(f"{self.prefix_url}/", args=params.to_dict())
        
        if resp is None:
            return None

        if isinstance(resp, list):
            events: list[Event] = [Event(card) for card in resp]
            
            return events
    
    def get_event_borders(self, event: int | Event) -> EventBorders | None:
        resp = self._client.get(f"{self.prefix_url}/{int(event)}/rankings/borders")
        
        if not resp:
            return None

        border_dict: EventBordersDict = cast(EventBordersDict, resp)

        return EventBorders(border_dict)
    
    def get_event_summaries(
            self, event: int | Event, type: str) -> list[EventSumm] | None:

        url = f"{self.prefix_url}/{int(event)}"
        resp = self._client.get(f"{url}/rankings/{type}/summaries")

        if not resp:
            return None
        
        if isinstance(resp, list):
            summaries = [EventSumm(summ) for summ in resp]

            return summaries
    
    def get_event_idol_summaries(
            self, event: int | Event,
            idol: int | Idol) -> list[EventSumm] | None:

        url = f"{self.prefix_url}/{int(event)}"
        
        if isinstance(idol, Idol):
            url += f"/rankings/idolPoint/{idol.id}/summaries"
        elif isinstance(idol, int):
            url += f"/rankings/idolPoint/{idol}/summaries"
        
        resp = self._client.get(url)

        if not resp:
            return None
        
        if isinstance(resp, list):
            summaries = [EventSumm(summ) for summ in resp]

            return summaries
    
    def get_event_logs(
            self, event: int | Event, type: str,
            ranks: list[int], since: datetime | None = None) -> list[EventLog] | None:

        url = f"{self.prefix_url}/{int(event)}/rankings/{type}/logs/"
        url += ",".join(str(i) for i in ranks)

        params = {"since": since} if since else None
        resp = self._client.get(url, args=params)

        if not resp:
            return None
        
        if isinstance(resp, list):
            logs = [EventLog(log) for log in resp]

            return logs
            