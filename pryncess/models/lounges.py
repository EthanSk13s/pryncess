class Lounge(object):
    def __init__(self, data: dict):
        self.id = data['id']
        self.view_id = data['viewerId']
        self.name = data['name']
        self.comment = data['comment']
        self.count = data['userCount']
        self.limit = data['userCountLimit']
        self.fan = data['fan']
        self.master = data['masterName']
        self.creation = data['createTime']
        self.update = data['updateTime']

class LoungeHistory(object):
    def __init__(self, data: dict):
        self.event_id = data['eventId']
        self.event_name = data['eventName']
        self.summary = data['sumamryTime']
        self.rank = data['rank']
        self.score = data['score']

class LoungeResults(object):
    def __init__(self, data: dict):
        self.id = data['id']
        self.view_id = data['viewerId']
        self.name = data['name']
        self.update= data['updateTime']