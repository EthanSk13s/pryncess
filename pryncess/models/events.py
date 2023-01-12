import typing

from .cards import Card

class EventSchedule(object):
    def __init__(self, data: dict):
        self.begin = data['beginAt']
        self.end = data['endAt']
        self.page_begin = data['pageOpenedAt']
        self.page_end = data['pageClosedAt']
        self.boost_begin = data['boostBeginAt']
        self.boost_end = data['boostEndAt']

class Item(object):
    def __init__(self, data: dict):
        self.name: typing.Union[str, None] = data['name']
        self.short_name: typing.Union[str, None] = data['shortName']

class Event(object):
    def __init__(self, data: dict):
        self.id: int = data['id']
        self.type: int = data['type']
        self.appeal: int = data['appealType']
        self.schedule = EventSchedule(data['schedule'])
        self.name: str = data['name']
        self.item = Item(data['item'])
        self.cards: typing.Union[list[Card], None]

        if 'cards' in data:
            cards = []
            for card in data['cards']:
                cards.append(Card(card))

            self.cards = cards
        else:
            self.cards = None

    def get_event_banner(self, event: 'Event'):
        url = f'https://storage.matsurihi.me/mltd/event_bg/{str(event.id).zfill(4)}.png'

        if event.id == 80:
            url = 'https://mltd.matsurihi.me/image/salmon/salmon_top_bg_01.png'
        elif event.id == 141:
            url = 'https://mltd.matsurihi.me/image/oyster/oyster_top_bg.png'

        return url

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
