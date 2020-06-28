import requests
import json
import time
from io import BytesIO
from typing import Optional

from .models import cards, events, lounges, elections, versions
from .name_finder import match_id, set_name, set_desc, set_center

class Client(object):
    def __init__(self, version, request_session=True, timeout=10):
        self.path = f"https://api.matsurihi.me/mltd/v1/{version}/"
        self.timeout = timeout
        self.retries = 5

        if isinstance(request_session, requests.Session):
            self._session = request_session
        else:
            if request_session:
                self._session = requests.Session()
            else:
                from requests import api
                self._session = api

    # This function is based off pyKirara so it's mostly the same
    def _internal_call(self, method, url, payload, params):
        args = dict(params=params)
        args['timeout'] = self.timeout

        if not url.startswith('http'):
            # If statement is for disabling pretty printing
            if '?' in url:
                arg = '&'
            else:
                arg = '?'
            url = self.path + url + arg +'prettyPrint=false'  # Disable pretty print, we don't need it

        if payload:
            args['data'] = json.dumps(payload)

        r = self._session.request(method, url, **args)

        try:
            r.raise_for_status()
        finally:
            r.connection.close()
        
        if r.headers['content-type'] == 'application/json; charset=utf-8':
            if r.text and len(r.text) > 0 and r.text != 'null':
                result = r.json()
                return result
            else:
                return None

        elif r.headers['content-type'] == 'image/png':

            return r.content

    def _get(self, url, args=None, payload=None, **kwargs):
        if args:
            kwargs.update(args)

        reconnect = self.timeout
        while reconnect > 0:
            try:
                return self._internal_call('GET', url, payload, kwargs)
            except:
                time.sleep(2)

class Pryncess(Client):
    def __init__(self, version):
        super().__init__(version)
        self.types = [
        'eventPoint',
        'highScore',
        'loungePoint'
        ]

    def get_latest(self):

        return versions.LatestVersion(self._get('version/latest'))

    def get_version(self, version: str):
        
        return versions.App(self._get(f'version/apps/{version}'))

    def get_assets(self, version: str):

        return versions.Res(self._get(f'version/assets/{version}'))

    def get_id(self, name: str):

        return match_id(name)

    def get_card(self, Id: Optional[int] = None,
    rarity: Optional[int] = None, extra_type: Optional[int] = None,
    is_idol=False, tl=True):
        params = {}
        # Check if we need to add additional parameters to request
        if is_idol:
            params['idolId'] = Id
        if extra_type:
            params['extraType'] = extra_type
        if rarity:
            params['rarity'] = rarity

        if params:
            raw_cards = self._get(f'cards', args=params)
            card = []

            for x in raw_cards:
                card_obj = cards.Card(x)
                if tl:
                    set_name(card_obj)
                    if card_obj.skill is not None:
                        set_desc(card_obj)
                    if card_obj.center_skill is not None:
                        set_center(card_obj)

                card.append(card_obj)
        elif Id:
            url = self._get(f'cards/{Id}')
            card = cards.Card(url[0])
            if tl:
                set_name(card)
                if card.skill is not None:
                    set_desc(card)
                if card.center_skill is not None:
                    set_center(card)
        else:
            msg = "No arguments were passed. (Id, rarity, or extra_type is required)"
            error = Exception(msg)
            raise error

        return card

    def get_image(self, card: 'Card', image_type: str,
    is_awake=False, background=False, get_url=False, stream=True):
        a = int(is_awake)
        b = ''
        # Determine whether to have background or not
        if image_type == 'card':
            if background:
                b = 'b'
            else:
                b = 'a'

        # Shorten url for PEP
        url = 'https://storage.matsurihi.me/mltd/'
        c = 'costume_icon_ll'

        image_types = {
            'card': f'{url}card/{card.resc_id}_{a}_{b}.png',
            'icon': f'{url}icon_l/{card.resc_id}_{a}.png',
        }

        if card.rarity != 4:
            image_types['card_bg'] = None
        else:
            image_types['card_bg'] = f'{url}card_bg/{card.resc_id}_{a}.png'

        if card.costume is None:
            image_types['costume'] = None
            image_types['bonus_costume'] = None
        else:
            costume = card.costume.resc_id
            if card.bonus_costume is not None:
                bonus_costume = card.bonus_costume.resc_id
            else:
                bonus_costume = None

            image_types['costume'] = f'{url}{c}/{costume}.png'
            image_types['bonus_costume'] = f'{url}{c}/{bonus_costume}.png'

        if card.rank_costume is None:
            image_types['rank_costume'] = None
        else:
            rank_costume = card.rank_costume.resc_id
            image_types['rank_costume'] = f'{url}{c}/{rank_costume}.png'

        image = image_types.get(image_type)

        if not get_url:
            if stream:
                return BytesIO(self._get(image))
            else:
                return self._get(image)
        else:
            return image

    def get_event(self, Id: int):
        
        return events.Event(self._get(f'events/{Id}'))

    def get_event_banner(self, event: 'Event', get_url=False):
        url = f'https://storage.matsurihi.me/mltd/event_bg/{str(event.id).zfill(4)}.png'
        banner = self._get(url)

        if get_url:
            return url
        else:
            return banner

    def get_borders(self, Id: int):
        borders = self._get(f'events/{Id}/rankings/borders')

        return events.EventBorders(borders)

    def get_event_summaries(self, Id: int, Type: str):
        if Type in self.types:
            summaries = self._get(f'events/{Id}/rankings/summaries/{Type}')
        summ_list = []
        
        for summary in summaries:
            summ_obj = events.EventSumm(summary)
            summ_list.append(summ_obj)

        return summ_list

    def get_event_logs(self, Id: int, Type: str, ranks: list):
        if Type in self.types:
            str_ranks = str(ranks).strip('[]').replace(' ', '')
            rank = self._get(f'events/{Id}/rankings/logs/{Type}/{str_ranks}')
        ranker_list = []

        for k in range(len(rank)):
            ranker = events.EventLog(rank[k])
            ranker_list.append(ranker)

        return ranker_list

    def get_event_idolpoints(self, Id: int, idol_id: int, ranks: list):
        str_ranks = str(ranks).strip('[]').replace(' ', '')
        rank = self._get(f'events/{Id}/rankings/logs/idolPoint/{idol_id}/{str_ranks}')
        ranker_list = []

        for k in range(len(rank)):
            ranker = events.EventLog(rank[k])
            ranker_list.append(ranker)

        return ranker_list

    def get_lounge(self, Id: str):

        return lounges.Lounge(self._get(f'lounges/{Id}'))

    def search_lounge(self, query: str):
        lounge_list = []
        search = self._get(f'lounges/search?name={query}')

        for lounge in search:
            lounge_list.append(lounges.LoungeResults(lounge))
 
        return lounge_list

    def get_lounge_eventhistory(self, Id: str):
        history_list = []
        histories = self._get(f'lounges/{Id}/eventHistory')

        for history in histories:
            history_list.append(lounges.LoungeHistory(history))

        return history_list 

    def get_election(self, is_current=False):
        if is_current:
            return elections.CurrentElection(self._get('election/current'))
        else:
            return elections.Election(self._get('election'))

    def get_all_cards(self, tl=False):
        card_list = self._get('cards')
        card_objs = []

        for card in card_list:
            card_objs.append(cards.Card(card))

        if tl:
            for obj in card_objs:
                set_name(obj)
                if obj.skill is not None:
                    set_desc(obj)
                if obj.center_skill is not None:
                    set_center(obj)

        return card_objs

    def current_event(self):
        current_event = self._get('events')[-1]

        return events.Event(current_event)

    def get_all_events(self):
        event_list = self._get('events')
        event_objs = []

        for event in event_list:
            event_objs.append(events.Event(event))

        return event_objs
