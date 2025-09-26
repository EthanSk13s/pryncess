import requests

from typing import cast

from pryncess.internals import Client
from pryncess.models.events import VotingEvent, VotingEventLogs
from pryncess.types.events import VotingEventDict


class VoteAPI:
    """Represents access to the voting data endpoint for the MLTD endpoint of the API.

    This class serves as a wrapper around requests to the voting data API. Allowing
    easy access and filtering for election and voting data throughout the game.

    Example:

    .. code-block:: py

        from pryncess.mltd.mltd_client import MLTDClient

        mltd = MLTDClient("ja")

        vote_api = mltd.vote_api()
        election = vote_api.get_votes(2)
    """
    def __init__(self, session: requests.Session):
        self.prefix_url = f"/mltd/v2/ja/votes" # Only JP has voting events.
        self._client = Client(session)
    
    def get_votes(self, id: int | None = None) -> list[VotingEvent] | None:
        """Fetches voting event data from the API.

        Retrieves one or more elections based on the provided ID.

        Args:
            id (:class:`int`, optional): Specific election ID to fetch. Defaults to None. If None,
                returns the entire list of existing elections.

        Returns:
            list[:class:`~pryncess.models.events.VotingEvent`] | None: A list of `VotingEvent` objects
            if results are found, or None if the request fails.
        """

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
        """Fetches voting event logs from the API.

        Args:
            event (:class:`~pryncess.models.events.VotingEvent` | :class:`int`): Specific election to fetch. Defaults to None.

        Returns:
            list[:class:`~pryncess.models.events.VotingEventLogs`] | None: A list of `VotingEventLogs` objects 
            if results are found, or None if the request fails.
        """

        resp = self._client.get(f"{self.prefix_url}/{int(event)}/rankings/logs")

        if not resp:
            return None
        
        if isinstance(resp, list):
            logs = [VotingEventLogs(log) for log in resp]

            return logs
