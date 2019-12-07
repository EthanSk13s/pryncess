class App(object):
    def __init__(self, data: dict):
        self.version = data['version']
        self.update = data['updateTime']
        self.revision = data['revision']

class Res(object):
    def __init__(self, data: dict):
        self.version = data['version']
        self.update = data['updateTime']
        self.index = data['indexName']

class LatestVersion(object):
    def __init__(self, data: dict):
        self.app = App(data['app'])
        self.res = Res(data['res'])