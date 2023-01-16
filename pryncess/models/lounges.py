class Master(object):
    def __init__(self, data: dict):
        self.name: str = data['name']
        self.icon: str = data['icon']

class LoungeHistory(object):
    def __init__(self, data: dict):
        self.event_id = data['eventId']
        self.event_name = data['eventName']
        self.summary = data['summaryTime']
        self.rank = data['rank']
        self.score = data['score']

class Lounge(object):
    def __init__(self, data: dict):
        self.id: int = data['id']
        self.view_id: str = data['viewerId']
        self.name: str = data['name']
        self.comment: str = data['comment']
        self.master: Master = Master(data['master'])
        self.fan: int = data['fan']
        self.rank: int = data['rank']
        self.play_style_type: int = data['playStyleType']
        self.mood_type: int = data['moodType']
        self.approval_type: int = data['approvalType']
        self.users: int = data['numUsers']
        self.users_limit: int = data['numUsersLimit']
        self.created_at = data['createdAt']
        self.updated_at = data['updatedAt']