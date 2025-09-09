from datetime import datetime
from typing import TypedDict

class AppDict(TypedDict):
    version: str
    updatedAt: datetime
    revision: int | None


class AssetDict(TypedDict):
    version: int
    updatedAt: datetime
    indexName: str

