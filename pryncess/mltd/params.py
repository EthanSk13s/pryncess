from dataclasses import dataclass

from datetime import datetime
from typing import Any, Self, Protocol

@dataclass
class Params(Protocol):
    def to_dict(self) -> dict[str, Any]:
        ...
    
    @classmethod
    def all(cls) -> Self:
        ...


@dataclass
class CardParams(Params):
    rarity: list[int] | None
    idols: list[int] | None
    extra_types: list[int] | None
    parameters: bool
    costumes: bool
    lines: bool
    skills: bool
    events: bool
    
    def to_dict(self) -> dict[str, Any]:
        params = {
            "exType": self.extra_types,
            "includeParameters": self.parameters,
            "includeLines": self.lines,
            "includeSkills": self.skills,
            "includeEvents": self.events
        }

        # Princess accepts a lists as comma separated values.
        # So we convert them from the list.
        if self.rarity:
            params["rarity"] = ",".join(str(rarity) for rarity in self.rarity)
        if self.idols:
            params["idolId"] = ",".join(str(id) for id in self.idols)
        if self.extra_types:
            params["exType"] = ",".join(str(type) for type in self.extra_types)

        return params

    @classmethod
    def all(cls) -> Self:
        card_params = cls(rarity=None,
                          idols=None,
                          extra_types=None,
                          parameters=True,
                          lines=True,
                          skills=True,
                          events=True,
                          costumes=True)
        
        return card_params


@dataclass
class EventParams(Params):
    event_type: list[int] | None
    event_at: datetime | None
    order_by: str | None
    desc: bool

    def to_dict(self) -> dict[str, Any]:
        params: dict[str, Any] = {
            "at": self.event_at,
            "orderBy": self.order_by
        }

        # Add an exclamation to sort in descending order per Princess docs.
        if self.order_by and self.desc:
            params["orderBy"] += "!"

        if self.event_type:
            params["type"] = ",".join(str(type) for type in self.event_type)
        
        return params
    
    @classmethod
    def all(cls) -> Self:
        return cls(event_type=None, event_at=None, order_by="beginAt", desc=False)
