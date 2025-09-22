from datetime import datetime

from pryncess.types.lounges import MasterDict, LoungeDict


class Master:
    """Represents the leader of a lounge.

    Attributes:
        name (:class:`str`): The username of the player.
        icon (:class:`str`): The card icon set by the player.
    """
    def __init__(self, data: MasterDict):
        self.name: str = data.get("name")
        self.icon: str = data.get("icon")


class Lounge:
    """Represents a lounge object returned from the Princess API.

    This class is initialized via a TypedDict representing the JSON response
    that the API returns. Therefore, you are not meant to manually initialize
    this class.

    Attributes:
        id (:class:`str`): The Actual UUID of the lounge.
        view_id (:class:`str`): The Viewer ID (8-digit Base32 lounge ID) of the lounge.
        name (:class:`str`): The name of the lounge.
        comment (:class:`str`): The comment of the lounge.
        master (:class:`Master`): The master / founder of the lounge.
        fan (:class:`int`): The number of total fans that the lounge has.
        rank (:class:`int`): The rank of the lounge. Ranges from 1-8.
        play_style_type (:class:`int`): The type of play style the lounge is. Ranges from 1-5.
        mood_type (:class:`int`): The mood of the lounge. Ranges from 1-5.
        approval_type (:class:`int`): The type of application the lounge has. Either 1 (Free to enter) or 2 (Approval).
        num_of_users (:class:`int`): The number of users in the lounge.
        users_limit (:class:`int`): The maximum number of users the lounge can have.
        created_at (:class:`int`): The date and time when the lounge was created.
        updated_at (:class:`int`): The date and time when the lougne was last updated.
    
    Hint:
        Casting an instance of :class:`Lounge` to a :class:`str` will return the lounge ID.
    """
    def __init__(self, data: LoungeDict):
        self.id: str = data.get("id")
        self.view_id: str = data.get("viewerId")
        self.name: str = data.get("name")
        self.comment: str = data.get("comment")
        self.master: Master = Master(data.get("master"))
        self.fan: int = data.get("fan")
        self.rank: int = data.get("rank")
        self.play_style_type: int = data.get("playStyleType")
        self.mood_type: int = data.get("moodType")
        self.approval_type: int = data.get("approvalType")
        self.num_of_users: int = data.get("numUsers")
        self.users_limit: int = data.get("numUsersLimit")
        self.created_at: datetime = data.get("createdAt")
        self.updated_at: datetime = data.get("updatedAt")
    
    def __str__(self):
        return self.id
