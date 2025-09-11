from dataclasses import dataclass

from typing import Any, Self, Protocol

@dataclass
class Params(Protocol):
    
    def to_dict(self) -> dict[str, Any]:
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