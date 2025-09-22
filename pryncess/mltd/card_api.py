import requests

from pryncess.internals import Client
from pryncess.models.cards import Card

from pryncess.mltd.params import CardParams


class CardAPI:
    """Represents access to the card endpoint for the MLTD endpoint of the API.

    This class serves as a wrapper around requests to the card API. Allowing
    easy access and filtering for what cards to retrieve.

    Example:

    .. code-block:: py

        from pryncess.mltd.mltd_client import MLTDClient
        from pryncess.mltd.params import CardParams

        mltd = MLTDClient("ja")

        client = mltd.card_api()

        # Enable the default parameters for cards.
        params = CardParams.all()

        # Set which idols to search for. (In this case, Tanaka Kotoha).
        params.idols = [17]

        # Set what rarities to filter for.
        params.rarity = [3, 4]

        cards = client.get_card(params)
    """

    def __init__(self, version: str, session: requests.Session):
        """Initializes the CardAPI instance.

        Args:
            version (str): API version string (e.g., "ja", "ko").
            session (requests.Session): A requests session used for making HTTP requests.
        """

        self.prefix_url = f"/mltd/v2/{version}/cards"
        self._client = Client(session)
    
    def get_card(self, params: CardParams, card_id: int | None = None) -> list[Card] | None:
        """Fetches card data from the API.

        Retrieves one or more cards based on the provided parameters. If a
        specific card ID is given, fetches that card; otherwise, retrieves
        all cards matching the query parameters.

        Args:
            params (CardParams): Query parameters for filtering card data.
            card_id (:class:`int`, optional): Specific card ID to fetch. Defaults to None.

        Returns:
            list[Card] | None: A list of `Card` objects if results are found, or
            None if the request fails.
        """

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
        """Fetches all available cards from the API.

        This method automatically uses default parameters to retrieve all
        card entries in the database.

        Returns:
            list[Card] | None: A list of all Card objects, or None if the request fails.
        """

        params = CardParams.all()

        return self.get_card(params)