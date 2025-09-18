from datetime import datetime
from pryncess.types.events import (
    EventDataDict,
    EventDict,
    EventBordersDict,
    EventIdolPtDict,
    EventLogDict,
    EventSummDict,
    ScheduleDict,
    ItemDict,
    EventLoungeDict,
    VotingEventRankingDict,
    VotingEventDict,
    VotingEventLogDict
)

from .cards import Card


class EventSchedule:
    """Represents the schedule of an event.

    This class contains various time specific information about
    the event.

    Attributes:
        begin (:class:`datetime.datetime`): Datetime of when the event begins.
        end (:class:`datetime.datetime`): Datetime of when the event ends.
        page_opened (:class:`datetime.datetime`): Datetime of when the event's page is opened in the game.
        page_closed (:class:`datetime.datetime`): Datetime of when the event's page is closed in the game.
        boost_begin (:class:`datetime.datetime` | `None`): Datetime of when event boosts starts if the event has one.
        boost_end (:class:`datetime.datetime` | `None`): Datetime of when event boosts ends.
    """
    def __init__(self, data: ScheduleDict):
        self.begin: datetime = data.get("beginAt")
        self.end: datetime = data.get("endAt")
        self.page_opened: datetime = data.get("pageOpenedAt")
        self.page_closed: datetime = data.get("pageClosedAt")
        self.boost_begin: datetime | None = data.get("boostBeginAt")
        self.boost_end: datetime | None = data.get("boostEndAt")


class Item:
    """Represents the item that an :class:`Event` uses for currency.

    Attributes:
        name (:class:`str` | `None`): The name of the item.
        short_name (:class:`str` | `None`): The short name of the item.
    """
    def __init__(self, data: ItemDict):
        self.name: str | None = data.get("name")
        self.short_name: str | None = data.get("shortName")


class Event:
    """Represent the Event response that the API returns.

    This class is initialized via a TypedDict representing the JSON response
    that the API returns. Therefore, you are not meant to manually initialize
    this class. Refer to Princess API documentation for more details for what
    each attribute means. Especially that of integer types.

    Attributes:
        id (:class:`int`): The ID for the event.
        type (:class:`int`): The type of the event. Ranges from 1-16.
        appeal (:class:`int`): The parameter that the event bonus is applied to. Ranges from 0-3.
        name (:class:`name`): The name of the event.
        schedule (:class:`EventSchedule`): The schedule for the event.
        item (:class:`Item`): The item for the event.
    Note:
        The attribute :class:`item` will never be `None`, but the name and short name can be `None`. Therefore
        if the name is `None`, then the item is `None`.
    Hint:
        Casting an instance of :class:`Event` to an :class:`int` will return the event ID.
    """
    def __init__(self, data: EventDict):
        self.id: int = data.get("id")
        self.type: int = data.get("type")
        self.appeal: int = data.get("appealType")
        self.name: str = data.get("name")
        self.schedule: EventSchedule = EventSchedule(data.get("schedule"))
        self.item: Item = Item(data.get("item"))

        cards = data.get("cards")
        if cards:
            self.cards = [Card(card) for card in cards]
        else:
            self.cards = None

    def get_event_banner(self, event: 'Event'):
        """Returns the URL for an Event's banner image.

        Returns:
            :class:`str`: The URL string of the banner.
        """
        url = f'https://storage.matsurihi.me/mltd/event_bg/{str(event.id).zfill(4)}.png'

        if event.id == 80:
            url = 'https://mltd.matsurihi.me/image/salmon/salmon_top_bg_01.png'
        elif event.id == 141:
            url = 'https://mltd.matsurihi.me/image/oyster/oyster_top_bg.png'

        return url
    
    def __int__(self):
        return self.id


class EventIdolPt:
    def __init__(self, data: EventIdolPtDict):
        self.idol_id: int = data.get("idolId")
        self.borders: list[int] = data.get("borders")


class EventBorders:
    def __init__(self, data: EventBordersDict):
        self.event_pt: list[int] | None = data.get("eventPoint")
        self.high_score: list[int] | None = data.get("highScore")
        self.high_score_2: list[int] | None = data.get("highScore2")
        self.high_score_total: list[int] | None = data.get("highScoreTotal")
        self.lounge_pt = data.get("loungePoint")

        idol_pts: list[EventIdolPtDict] | None = data.get("idolPoint")
        if idol_pts:
            rankings: list[EventIdolPt] | None = []
            for idol in idol_pts:
                rankings.append(EventIdolPt(idol))

            self.idol_pt: list[EventIdolPt] | None = rankings
        else:
            self.idol_pt = None


class EventSumm:
    def __init__(self, data: EventSummDict):
        self.count: int = data.get("count")
        self.sum_time: datetime | None = data.get("aggregatedAt")

        updated: datetime | None = data.get("updatedAt")
        if updated:
            self.updated: datetime | None = updated
        else:
            self.updated = None


class EventData:
    def __init__(self, data: EventDataDict):        
        self.score = data.get("score")
        self.aggregated = data.get("aggregatedAt")


class EventLog:
    def __init__(self, data: EventLogDict):
        self.rank = data.get("rank")
        self.data: list[EventData] = []

        for event_data in data.get("data"):
            self.data.append(EventData(event_data))


class LoungeHistory:
    def __init__(self, data: EventLoungeDict):
        self.event: Event = Event(data.get("event"))
        self.rank = data.get("rank")
        self.score = data.get("score")


class VotingEvent:
    def __init__(self, data: VotingEventDict):
        self.id: int = data.get("id")
        self.vote_type: int = data.get("voteSystemType")
        self.event: Event = Event(data.get("event"))
    
    def __int__(self):
        return self.id


class VotingEventRanking:
    def __init__(self, data: VotingEventRankingDict) -> None:
        self.candidate_id: str = data.get("candidateId")
        self.rank: int = data.get("rank")
        self.point: int = data.get("point")


class VotingEventLogs:
    def __init__(self, data: VotingEventLogDict):
        self.aggregated: datetime = data.get("aggregatedAt")
        self.updated: datetime = data.get("updatedAt")
        self.ranking: list[VotingEventRanking] = []

        for rank in data.get("ranking"):
            self.ranking.append(VotingEventRanking(rank))

