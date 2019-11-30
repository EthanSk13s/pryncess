class App(object):
    def __init__(self, data: dict):
        self.version = data['version']
        self.update = data['updateTime']
        self.revision = data['revision']

# TODO: Inherit from App instead
class Res(object):
    def __init__(self, data: dict):
        self.version = data['version']
        self.update = data['updateTime']
        self.index = data['indexName']