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
        self.item: Item = Item(data['item'])
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
        self.idol_id: int = data['idolId']
        self.borders: list[int] = data['borders']

class EventBorders(object):
    def __init__(self, data: dict):
        self.event_pt: typing.Union[list[int], None] = data['eventPoint'] if 'eventPoint' in data else None
        self.high_score: typing.Union[list[int], None] = data['highScore'] if 'highScore' in data else None
        self.high_score_2: typing.Union[list[int], None] = data['highScore2'] if 'highScore2' in data else None
        self.high_score_total: typing.Union[list[int], None] = data['highScoreTotal'] if 'highScoreTotal' in data else None
        self.lounge_pt: typing.Union[list[int], None] = data['loungePoint'] if 'loungePoint' in data else None
        self.idol_pt: typing.Union[list[EventIdolPt], None]

        if 'idolPoint' in data:
            rankings = []
            for idol in data['idolPoint']:
                rankings.append(EventIdolPt(idol))

            self.idol_pt = rankings
        else:
            self.idol_pt = None

class EventSumm(object):
    def __init__(self, data: dict):
        self.sum_time = data['aggregatedAt']
        if 'updatedAt' in data:
            self.update_time = data['updatedAt']
        else:
            self.update_time = None
        self.count = data['count']

class EventData(object):
    def __init__(self, data: dict):        
        self.score = data['score']
        self.summ_time = data['aggregatedAt']


class EventLog(object):
    def __init__(self, data: dict):
        self.rank = data['rank']
        self.data = {}

        for i in range(len(data['data'])):
            self.data[i] = EventData(data['data'][i])
