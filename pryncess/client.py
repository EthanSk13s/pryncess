import requests
import json
import time
from typing import Optional

from .models import cards, events, lounges, elections, versions, consts

class Client(object):
    def __init__(self, version, request_session=True, timeout=10):
        self.path = f"https://api.matsurihi.me/api/mltd/v2/{version}/"
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
            # Disable pretty print, we don't need it
            url = self.path + url + arg +'prettyPrint=false'

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

        return consts.match_id(name)

    def get_card(
            self, Id: Optional[int] = None,
            rarity: Optional[list[int]] = None, extra_type: Optional[list[int]] = None,
            include_costumes: Optional[bool] = None,
            include_parameters: Optional[bool] = None,
            include_lines: Optional[bool] = None,
            include_skills: Optional[bool] = None,
            include_events: Optional[bool] = None,
            is_idol=False, tl=True) -> list[cards.Card]:

        params = Pryncess._construct_params(rarity=rarity,
                                            ex_type=extra_type,
                                            include_costumes=include_costumes,
                                            include_parameters=include_parameters,
                                            include_lines=include_lines,
                                            include_skills=include_skills,
                                            include_events=include_events)

        if params:
            if Id:
                raw_cards = self._get(f'cards/{Id}', args=params)
            else:
                raw_cards = self._get('cards', args=params)
            card = []

            for x in raw_cards:
                card_obj = cards.Card(x)
                if tl:
                    consts.set_name(card_obj)
                    if card_obj.skill is not None:
                        card_obj.skill.tl_desc()
                    if card_obj.center_skill is not None:
                        card_obj.center_skill.tl_desc()

                card.append(card_obj)
        else:
            msg = "No arguments were passed. (Id, rarity, or extra_type is required)"
            error = Exception(msg)
            raise error

        return card

    def get_event(self, Id: int):
    
        return events.Event(self._get(f'events/{Id}'))

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
            rank = self._get(f'events/{Id}/rankings/{Type}/logs/{str_ranks}')
        ranker_list = []

        for k in range(len(rank)):
            ranker = events.EventLog(rank[k])
            ranker_list.append(ranker)

        return ranker_list

    def get_event_idolpoints(self, Id: int, idol_id: int, ranks: list):
        str_ranks = str(ranks).strip('[]').replace(' ', '')
        rank = self._get(f'events/{Id}/rankings/idolPoint/{idol_id}/logs/{str_ranks}')
        ranker_list = []

        for k in range(len(rank)):
            ranker = events.EventLog(rank[k])
            ranker_list.append(ranker)

        return ranker_list

    def get_lounge(self, Id: str):

        return lounges.Lounge(self._get(f'lounges/{Id}'))

    def search_lounge(self, query: str) -> list[lounges.Lounge]:
        lounge_list = []
        search = self._get(f'lounges?name={query}')

        for lounge in search:
            lounge_list.append(lounges.Lounge(lounge))
 
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
                consts.set_name(obj)
                if obj.skill is not None:
                    obj.skill.tl_desc()
                if obj.center_skill is not None:
                    obj.center_skill.tl_desc()

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

    @classmethod
    def _construct_params(self, **kwargs):
        params = {}
        if kwargs['rarity']:
            params['rarity'] = kwargs['rarity']
        if kwargs['include_costumes']:
            params['includeCostumes'] = kwargs['include_costumes']
        if kwargs['ex_type']:
            params['exType'] = kwargs['ex_type']
        if kwargs['include_parameters']:
            params['includeParameters'] = kwargs['include_parameters']
        if kwargs['include_lines']:
            params['includeLines'] = kwargs['include_lines']
        if kwargs['include_skills']:
            params['includeSkills'] = kwargs['include_skills']
        if kwargs['include_events']:
            params['includeEvents'] = kwargs['include_events']

        return params
