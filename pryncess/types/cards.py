from datetime import datetime
from typing import TypedDict, NamedTuple, Any


class CostumeDict(TypedDict):
    id: int
    sortId: int | None
    name: str | None
    description: str | None
    resourceId: str | None
    modelId: str | None
    costumeGroupId: int | None
    collaborationNumber: int | None
    defaultHairstyle: int | None
    releasedAt: datetime | None


class CardCostumes(TypedDict):
    default: CostumeDict | None
    bonus: CostumeDict | None
    rank5: CostumeDict | None


class CenterEffectDict(TypedDict):
    name: str
    id: int
    idolType: int
    description: str | None
    specificIdolType: int | None
    songType: int | None
    attributes: list[int]
    values: list[int]


class SkillDict(TypedDict):
    id: int
    effectId: int
    duration: int
    interval: int
    probability: int
    evaluations: list[int]
    values: list[int]
    description: str


class StatValues(NamedTuple):
    diff: int
    max: int

class StatsDict(TypedDict):
    base: int
    beforeAwakened: dict[str, int]
    afterAwakened: dict[str, int]
    masterBonus: int


class ParameterDict(TypedDict):
    vocal: StatsDict
    dance: StatsDict
    visual: StatsDict
    lvMax: dict[str, int]
    life: dict[str, int]


class CardDict(TypedDict):
    id: int
    name: str
    sortId: int
    idolId: int
    idolType: int
    resourceId: str
    rarity: int
    extraType: int
    category: int
    masterRankMax: int
    addedAt: datetime
    event: Any  # TODO: Implement Event and card lines
    skillLvMax: int
    skillName: str | None
    skills: list[SkillDict] | None
    parameters: ParameterDict | None
    centerEffect: CenterEffectDict | None
    costumes: CardCostumes | None