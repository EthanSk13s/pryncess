import requests

from typing import cast

from pryncess.internals import Client
from pryncess.models.idols import Idol
from pryncess.types.idols import IdolDict


class IdolAPI:
    """Represents access to the card endpoint for the MLTD endpoint of the API.

    This class serves as a wrapper around requests to the Idol API. Allowing
    access to a character's information.

    Example:

    .. code-block:: py

        from pryncess.mltd.mltd_client import MLTDClient
        from pryncess.mltd.params import CardParams

        mltd = MLTDClient("ja")

        client = mltd.idol_api()

        # Kotoha's ID.
        kth = client.get_idol(17)

        print(kth.alpha_name)
    """
    def __init__(self, version: str, session: requests.Session):
        self.prefix_url = f"/mltd/v2/{version}/idols"
        self._client = Client(session)
    
    def get_idol(self, idol_id: int) -> Idol | None:
        """Fetches idol data from the API.

        Args:
            idol_id (:class:`int`, optional): Specific idol ID to fetch

        Returns:
            :class:`~pryncess.models.idols.Idol` | None: An instance of an Idol. Returns None
            if the ID does not match anything.
        """
        resp = self._client.get(f"{self.prefix_url}/{idol_id}")

        if resp is None:
            return None

        idol_dict: IdolDict = cast(IdolDict, resp)

        return Idol(idol_dict)
