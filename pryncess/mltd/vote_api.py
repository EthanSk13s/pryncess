import requests

from typing import cast

from pryncess.internals import Client
from pryncess.models.events import VotingEvent, VotingEventLogs
from pryncess.types.events import VotingEventDict


class VoteAPI:
    def __init__(self, session: requests.Session):
        self.prefix_url = f"/mltd/v2/ja/votes" # Only JP has voting events.
        self._client = Client(session)
    
    def get_votes(self, id: int | None = None) -> list[VotingEvent] | None:
        if id:
            resp = self._client.get(f"{self.prefix_url}/{id}")
        else:
            resp = self._client.get(f"{self.prefix_url}/")
        
        if not resp:
            return None
        
        if isinstance(resp, list):
            events = [VotingEvent(event) for event in resp]

            return events
        else:
            event = cast(VotingEventDict, resp)

            return [VotingEvent(event)]
    
    def get_vote_logs(self, event: VotingEvent | int) -> list[VotingEventLogs] | None:
        resp = self._client.get(f"{self.prefix_url}/{int(event)}/rankings/logs")

        if not resp:
            return None
        
        if isinstance(resp, list):
            logs = [VotingEventLogs(log) for log in resp]

            return logs
