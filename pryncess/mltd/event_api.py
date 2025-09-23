import requests

from datetime import datetime
from typing import cast

from pryncess.internals import Client
from pryncess.models.idols import Idol
from pryncess.models.events import Event, EventBorders, EventSumm, EventLog
from pryncess.mltd.params import EventParams
from pryncess.types.events import EventBordersDict


class EventAPI:
    """Represents access to the event endpoints for the MLTD endpoint of the API.

    This class serves as a wrapper around requests to the event API. Allowing
    easy access and filtering for what event data throughout the game.

    Example:

    .. code-block:: py

        from pryncess.mltd.mltd_client import MLTDClient
        from pryncess.mltd.params import CardParams

        mltd = MLTDClient("ja")

        event_client = mltd.event_api()

        # Enable the default parameters for cards.
        event_params = EventParams.all()

        # Filter for specific event types.
        event_params.event_type = [4, 9, 11, 13]

        # Sort by descending.
        event_params.desc = True
        events = event_client.get_events(event_params)
    """
    def __init__(self, version: str, session: requests.Session):
        self.prefix_url = f"/mltd/v2/{version}/events"
        self._client = Client(session)
    
    def get_events(
            self, params: EventParams,
            event_id: int | None = None) -> list[Event] | None:
        """Fetches event data from the API.

        Retrieves one or more events based on the provided parameters. If a
        specific event ID is given, fetches that event; otherwise, retrieves
        all events matching the query parameters.

        Args:
            params (:class:`~pryncess.mltd.params.EventParams`): Query parameters for filtering event data.
            event_id (:class:`int`, optional): Specific event ID to fetch. Defaults to None.

        Returns:
            list[:class:`~pryncess.models.events.Event`] | None: A list of :class:`~pryncess.models.events.Event`
            objects if results are found, or None if the request fails.
        """
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
        """Retrieves tier border data from a specific event.

        Args:
            event (:class:`int` | :class:`~pryncess.models.events.Event`): Specific event to fetch for.

        Returns:
            :class:`~pryncess.models.events.EventBorders` | None: An EventBorders object if results are found, or
            None if the request fails.
        """
        resp = self._client.get(f"{self.prefix_url}/{int(event)}/rankings/borders")
        
        if not resp:
            return None

        border_dict: EventBordersDict = cast(EventBordersDict, resp)

        return EventBorders(border_dict)
    
    def get_event_summaries(
            self, event: int | Event, type: str) -> list[EventSumm] | None:
        """Retrieves participating player count from a specific event throughout its duration.

        Args:
            event (:class:`int` | :class:`~pryncess.models.events.Event`): Specific event to fetch for.
            type (:class:`str`): Type of ranking to fetch.
                Valid types are:
                    - eventPoint 
                    - highScore
                    - highScore2
                    - highScoreTotal 
                    - loungePoint

        Returns:
            :class:`~pryncess.models.events.EventSumm` | None: An EventSumm object if results are found, or
            None if the request fails.
        """

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
        """Retrieves participating player count for an idol from an anniversary event throughout its duration.

        Args:
            event (:class:`int` | :class:`~pryncess.models.events.Event`): Specific event to fetch for.
            idol (:class:`int` | :class:`~pryncess.models.idols.Idol`): Specific idol to fetch for.

        Returns:
            :class:`~pryncess.models.events.EventSumm` | None: An EventSumm object if results are found, or
            None if the request fails.
        """

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
        """Retrieves event logs from a specific event throughout its duration.

        Args:
            event (:class:`int` | :class:`~pryncess.models.events.Event`): Specific event to fetch for.
            type (:class:`str`): Type of ranking to fetch.
                Valid types are:
                    - eventPoint 
                    - highScore
                    - highScore2
                    - highScoreTotal 
                    - loungePoint

            ranks (:class:`int`): A list of specific ranks to query for.
            since (:class:`datetime.datetime`): Start time of the logs to fetch.

        Returns:
            :class:`~pryncess.models.events.EventLog` | None: An EventLog object if results are found, or
            None if the request fails.
        """

        url = f"{self.prefix_url}/{int(event)}/rankings/{type}/logs/"
        url += ",".join(str(i) for i in ranks)

        params = {"since": since} if since else None
        resp = self._client.get(url, args=params)

        if not resp:
            return None
        
        if isinstance(resp, list):
            logs = [EventLog(log) for log in resp]

            return logs
            