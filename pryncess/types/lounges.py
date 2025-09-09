from datetime import datetime
from typing import TypedDict


class MasterDict(TypedDict):
    name: str
    icon: str


class LoungeDict(TypedDict):
    id: str
    viewerId: str
    name: str
    comment: str
    master: MasterDict
    fan: int
    rank: int
    playStyleType: int
    moodType: int
    approvalType: int
    numUsers: int
    numUsersLimit: int
    createdAt: datetime
    updatedAt: datetime
