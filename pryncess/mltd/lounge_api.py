import requests

from typing import cast

from pryncess.internals import Client
from pryncess.models.lounges import Lounge
from pryncess.types.lounges import LoungeDict


class LoungeAPI:
    """Represents access to the lounge endpoint for the MLTD endpoint of the API.

    This class serves as a wrapper around requests to the lounge API. Allowing
    searching and accessing lounge information in the game.

    Example:

    .. code-block:: py

        from pryncess.mltd.mltd_client import MLTDClient
        from pryncess.mltd.params import CardParams

        mltd = MLTDClient("ja")

        lounge_client = mltd.lounge_api()
        lounge = lounge_client.get_lounge("751cba08-12c2-4282-b3aa-373035301b2e")
    """
    def __init__(self, version: str, session: requests.Session):
        self.prefix_url =  f"/mltd/v2/{version}/lounges" 
        self._client = Client(session)
    
    def get_lounge(self, lounge: str | Lounge) -> Lounge | None:
        """Retrieves lounge information based on a provided UUID.

        Args:
            lounge (:class:`str` | :class:`~pryncess.models.lounges.Lounge`): Specific lounge UUID to fetch for.

        Returns:
            :class:`~pryncess.models.lounges.Lounge` | None: A Lounge object if results are found, or
            None if the request fails.
        """
        resp = self._client.get(f"{self.prefix_url}/{str(lounge)}")

        if not resp:
            return None
        
        cast_lounge = cast(LoungeDict, resp)

        return Lounge(cast_lounge)
    
    def search_lounge(self, name: str) -> list[Lounge] | None:
        """Retrieves lounges based on a search query.

        Args:
            name (:class:`str`): Specific name to query for.

        Returns:
            :class:`~pryncess.models.lounges.Lounge` | None: A Lounge object if results are found, or
            None if the request fails.
        """
        args = {"name": name}
        resp = self._client.get(f"{self.prefix_url}", args=args)

        if not resp:
            return None
        
        if isinstance(resp, list):
            results = [Lounge(lounge) for lounge in resp]

            return results