class Roles(object):
    def __init__(self, data: dict):
        self.id = data['roles']
        self.name = data['name']

class Dramas(object):
    def __init__(self, data: dict):
        self.id = data['id']
        self.name = data['name']
        self.roles = Roles(data['roles'])

class Schedule(object):
    def __init__(self, data: dict):
        self.begin = data['beginDate']
        self.end = data['endDate']
        self.page_begin = data['pageBeginDate']
        self.page_end = data['pageEndDate']
        self.result_date = data['resultOpenDate']

class Election(object):
    def __init__(self, data: dict):
        self.id = data['id']
        self.name = data['name']
        self.schedule = Schedule(data['schedule'])
        self.dramas = Dramas(data['dramas'])

class ElectionData(object):
    def __init__(self, data: dict):
        self.idol_id = data['idolId']
        self.idol_name = data['idolName']
        self.score = data['score']
        self.rank = data['rank']

class CurrentElection(object):
    def __init__(self, data: dict):
        self.id = data['id']
        self.name = data['name']
        self.summ_time = data['summaryTime']
        self.data = data['data']
