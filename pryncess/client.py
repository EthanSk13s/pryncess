import requests
import json
from io import BytesIO
from typing import Optional

from .models import cards
from .name_finder import match_id, set_name

class Client(object):
    def __init__(self, request_session=True, timeout=10):
        self.path = "https://api.matsurihi.me/mltd/v1/"
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
            except Exception as e:
                raise print('exception:', str(e))

class Pryncess(Client):
    def __init__(self):
        super().__init__()
        self.types = [
        'eventPoint',
        'highScore',
        'loungePoint'
        ]

    def get_latest(self):

        return self._get('version/latest')

    def get_version(self, version: str):
        
        return self._get(f'version/apps/{version}')

    def get_assets(self, version: str):

        return self._get(f'version/assets/{version}')

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

                card.append(card_obj)
        elif Id:
            url = self._get(f'cards/{Id}')
            card = cards.Card(url[0])
            if tl:
                set_name(card)
        else:
            msg = "No arguments were passed. (Id, rarity, or extra_type is required)"
            error = Exception(msg)
            raise error

        return card

    def get_image(self, card: 'Card', image_type: str,
    is_awake=False, stream=True):
        a = int(is_awake)
        # Shorten url for PEP
        url = 'https://storage.matsurihi.me/mltd/'
        c = 'costume_icon_ll'

        image_types = {
            'card': f'{url}card/{card.resc_id}_{a}.png',
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
            bonus_costume = card.bonus_costume.resc_id

            image_types['costume'] = f'{url}{c}/{costume}.png'
            image_types['bonus_costume'] = f'{url}{c}/{bonus_costume}.png'

        if card.rank_costume is None:
            image_types['rank_costume'] = None
        else:
            rank_costume = card.rank_costume.resc_id
            image_types['rank_costume'] = f'{url}{c}/{rank_costume}.png'

        image = image_types.get(image_type)

        if stream:
            return BytesIO(self._get(image))
        else:
            return self._get(image)

    def get_event(self, Id: int):
        
        return self._get(f'events/{Id}')

    def get_borders(self, Id: int):

        return self._get(f'events/{Id}/rankings/borders')

    def get_event_summaries(self, Id: int, Type: str):
        if Type in self.types:
            return self._get(f'events/{Id}/rankings/summaries/{Type}')

    def get_event_logs(self, Id: int, Type: str, ranks: list):
        if Type in self.types:
            str_ranks = str(ranks).strip('[]').replace(' ', '')
            return self._get(f'events/{Id}/rankings/logs/{Type}/{str_ranks}')

    def get_event_idolpoints(self, Id: int, idol_id: int, ranks: list):
        str_ranks = str(ranks).strip('[]').replace(' ', '')

        return self._get(f'events/{Id}/rankings/logs/idolPoint/{idol_id}/{str_ranks}')

    def get_lounge(self, Id: int):

        return self._get(f'lounges/{Id}')

    def search_lounge(self, query: str):

        return self._get(f'lounges/search?name={query}')

    def get_lounge_eventhistory(self, Id: int):

        return self._get(f'lounges/{Id}/eventHistory')

    def get_election(self, is_current=False):
        if is_current:
            return self._get('election/current')
        else:
            return self._get('election')
