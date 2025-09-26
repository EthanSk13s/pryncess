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
    """Represents a wrapper to various filters and options when searching for cards.

    This class is usually initialized via `.all()`, and each attribute can be modified
    to fine-tune what data is needed. An instance of this class is passed to the Card API
    to easily filter cards.

    Attributes:
        rarity (list[:class:`int`] | `None`): A list of rarities to filter for.
            If this is None, then all rarities will be included.
        idols (list[:class:`int`] | `None`): A list of idols to filter for. 
            If this is None, then all idols will be included.
        extra_types (list[:class:`int`] | `None`): A list of extra types to filter for.
            If this is None, then all types will be included.
        parameters (:class:`bool`): A boolean value to determine whether to include parameter data.
        costumes (:class:`bool`): A boolean value to determine whether to include costume data.
        lines (:class:`bool`): A boolean value to determine whether to include lines for the cards.
        skills (:class:`bool`): A boolean value to determine whether to include skills data.
        events (:class:`bool`): A boolean value to determine whether to include event data to cards that apply.
    
    Example:

    .. code-block:: py

        from pryncess.mltd.params import CardParams

        # Enable the default parameters for cards.
        params = CardParams.all()

        # Set which idols to search for. (In this case, Tanaka Kotoha).
        params.idols = [17]

        # Set what rarities to filter for.
        params.rarity = [3, 4]
    """

    rarity: list[int] | None
    idols: list[int] | None
    extra_types: list[int] | None
    parameters: bool
    costumes: bool
    lines: bool
    skills: bool
    events: bool
    
    def to_dict(self) -> dict[str, Any]:
        """Converts an instance to a dict.

        This is usually used for handling the arguments for the GET request for the API.

        Returns:
            dict[:class:`str`, :class:`Any`]: A dict representing the mappings to the values.
        """
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
        """Returns an instance with no filters, and all options enabled.
        """
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
    """Represents a wrapper to various filters and options when searching for events.

    This class is usually initialized via `.all()`, and each attribute can be modified
    to fine-tune what data is needed. An instance of this class is passed to the Event API
    to easily filter events.

    Attributes:
        event_type (list[:class:`int`] | `None`): A list of event types to filter for.
            If this is None, then all types will be included.
        event_at (:class:`datetime.datetime` | `None`): A datetime for an event held at the specified date and time.
        order_by (list[:class:`int`] | `None`): The sort order for the events. Valid sort keys are:

            - "id"
            - "type"
            - "beginAt"

        desc (:class:`bool`): A boolean value whether to order by descending.
        
    Example:

    .. code-block:: py

        from pryncess.mltd.params import EventParams

        # Create an instance will all options enabled.
        event_params = EventParams.all()

        # Filter for specific event types based on the event type ID.
        event_params.event_type = [4, 9, 11, 13]

        # Enable ordering by descending
        event_params.desc = True
    """
    event_type: list[int] | None
    event_at: datetime | None
    order_by: str | None
    desc: bool

    def to_dict(self) -> dict[str, Any]:
        """Converts an instance to a dict.

        This is usually used for handling the arguments for the GET request for the API.

        Returns:
            dict[:class:`str`, :class:`Any`]: A dict representing the mappings to the values.
        """
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
        """Returns an instance with no filters, and all options enabled.
        """
        return cls(event_type=None, event_at=None, order_by="beginAt", desc=False)
