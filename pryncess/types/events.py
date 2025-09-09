from datetime import datetime
from typing import TypedDict

from pryncess.types.cards import CardDict


class ScheduleDict(TypedDict):
    beginAt: datetime
    endAt: datetime
    pageOpenedAt: datetime
    pageClosedAt: datetime
    boostBeginAt: datetime | None
    boostEndAt: datetime | None


class ItemDict(TypedDict):
    name: str | None
    shortName: str | None


class EventDict(TypedDict):
    id: int
    type: int
    appealType: int
    name: str
    schedule: ScheduleDict
    item: ItemDict
    cards: list[CardDict]


class EventIdolPtDict(TypedDict):
    idolId: int
    borders: list[int]


class EventBordersDict(TypedDict):
    eventPoint: list[int] | None
    highScore: list[int] | None
    highScore2: list[int] | None
    highScoreTotal: list[int] | None
    loungePoint: list[int] | None
    idolPoint: list[EventIdolPtDict] | None


class EventSummDict(TypedDict):
    count: int
    aggregatedAt: datetime | None
    updatedAt: datetime | None


class EventDataDict(TypedDict):
    score: int
    aggregatedAt: datetime


class EventLogDict(TypedDict):
    rank: int
    data: list[EventDataDict]


class EventLoungeDict(TypedDict):
    rank: int
    score: int
    event: EventDict