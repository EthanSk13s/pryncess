import requests

from pryncess.mltd.card_api import CardAPI
from pryncess.mltd.event_api import EventAPI
from pryncess.mltd.lounge_api import LoungeAPI
from pryncess.mltd.vote_api import VoteAPI

class MLTDClient:
    def __init__(self, version: str):
        self.session = requests.Session()
        self.version = version
    
    def card_api(self) -> CardAPI:

        return CardAPI(self.version, self.session)
    
    def event_api(self) -> EventAPI:

        return EventAPI(self.version, self.session)
    
    def vote_api(self) -> VoteAPI:

        return VoteAPI(self.session)
    
    def lounge_api(self) -> LoungeAPI:

        return LoungeAPI(self.version, self.session)