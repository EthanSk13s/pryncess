import requests

from dataclasses import dataclass
from typing import Any, Self

from pryncess.internals import Client
from pryncess.models.cards import Card

@dataclass
class CardParams:
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


class CardAPI:
    def __init__(self, version: str, session: requests.Session):
        self.prefix_url = f"/mltd/v2/{version}/cards"
        self._client = Client(session)
    
    def get_card(self, params: CardParams, card_id: int | None = None) -> list[Card] | None:
        if card_id:
            resp = self._client.get(f"{self.prefix_url}/{card_id}", args=params.to_dict())
        else:
            resp = self._client.get(f"{self.prefix_url}/", args=params.to_dict())

        if resp is None:
            return None
        
        if isinstance(resp, list):
            cards: list[Card] = [Card(card) for card in resp]
            
            return cards
    
    def get_all_cards(self) -> list[Card] | None:
        params = CardParams.all()

        return self.get_card(params)