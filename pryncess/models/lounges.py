from pryncess.types.lounges import MasterDict, LoungeDict


class Master:
    def __init__(self, data: MasterDict):
        self.name: str = data.get("name")
        self.icon: str = data.get("icon")


class Lounge:
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
        self.created_at = data.get("createdAt")
        self.updated_at = data.get("updatedAt")
