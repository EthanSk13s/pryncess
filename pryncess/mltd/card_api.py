import requests

from pryncess.internals import Client
from pryncess.models.cards import Card

from pryncess.mltd.params import CardParams


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