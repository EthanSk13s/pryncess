import requests

from pryncess.mltd.card_api import CardAPI
from pryncess.mltd.event_api import EventAPI
from pryncess.mltd.lounge_api import LoungeAPI
from pryncess.mltd.vote_api import VoteAPI

class MLTDClient:
    """Represents the entry point of the MLTD endpoints.

    This class creates a session and manages which version the library will used.
    Each function will use the session created by an instance of this class.

    Attributes:
        session (:class:`requests.Session`): The requests session that the endpoints will use.
        version (:class:`str`): Which version that the endpoints will use. ('ja', 'ko', or 'zh').
    """
    def __init__(self, version: str):
        self.session = requests.Session()
        self.version = version
    
    def card_api(self) -> CardAPI:
        """Returns an instance of CardAPI.

        Returns:
            CardAPI: An instance of CardAPI.
        """

        return CardAPI(self.version, self.session)
    
    def event_api(self) -> EventAPI:
        """Returns an instance of EventAPI.

        Returns:
            EventAPI: An instance of EventAPI.
        """

        return EventAPI(self.version, self.session)
    
    def vote_api(self) -> VoteAPI:
        """Returns an instance of VoteAPI.

        Returns:
            VoteAPI: VoteAPI.
        """

        return VoteAPI(self.session)
    
    def lounge_api(self) -> LoungeAPI:
        """Returns an instance of LoungeAPI.

        Returns:
            LoungeAPI: An instance of LoungeAPI.
        """

        return LoungeAPI(self.version, self.session)