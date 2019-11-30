class EventSchedule(object):
    def __init__(self, data: dict):
        self.begin = data['beginDate']
        self.end = data['endDate']
        self.page_begin = data['pageBeginDate']
        self.page_end = data['pageEndDate']

        if 'boostBeginDate' in data:
            self.boost_begin = data['boostBeginDate']
            self.boost_end = data['boostEndDate']
        else:
            self.boost_begin = None
            self.boost_end = None

class Event(object):
    def __init__(self, data: dict):
        self.id = data['id']
        self.type = data['type']
        if 'appealType' in data:
            self.appeal = data['appealType']
        else:
            self.appeal = None

        self.schedule = EventSchedule(data['schedule'])
        self.name = data['name']

class EventIdolPt(object):
    def __init__(self, data: dict):
        self.idol_id = data['idolId']
        self.borders = data['borders']

class EventBorders(object):
    def __init__(self, data: dict):
        self.event_pt = data['eventPoint']
        self.high_score = data['highScore']
        self.lounge_pt = data['loungePoint']

        if 'idolPoint' in data:
            self.idol_pt = EventIdolPt(data['idolPoint'])
        else:
            self.idol_pt = None

class EventSumm(object):
    def __init__(self, data: dict):
        self.sum_time = data['summaryTime']
        if 'updateTime' in data:
            self.update_time = data['updateTime']
        else:
            self.update_time = None
        self.count = data['count']

class EventData(object):
    def __init__(self, data: dict):        
        self.score = data['score']
        self.summ_time = data['summaryTime']


class EventLog(object):
    def __init__(self, data: dict):
        self.rank = data['rank']
        self.data = {}

        for i in range(len(data['data'])):
            self.data[i] = EventData(data['data'][i])