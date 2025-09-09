from pryncess.types.versions import AppDict, AssetDict


class App:
    def __init__(self, data: AppDict):
        self.version = data.get("version")
        self.update = data.get("updatedAt")
        self.revision = data.get("revision")


class Res(object):
    def __init__(self, data: AssetDict):
        self.version = data.get("version")
        self.update = data.get("updatedAt")
        self.index = data.get("indexName")


class LatestVersion(object):
    def __init__(self, data: dict):
        app = data.get("app")
        if app is not None:
            self.app = App(app)
        else:
            self.app = None

        res = data.get("res")
        if res is not None:
            self.res = Res(res)
        else:
            self.res = None