from typing import TypedDict


class MiscDataDict(TypedDict):
    id: int
    name: str


class BirthdayDict(TypedDict):
    month: int
    day: int


class MeasurementsDict(TypedDict):
    bust: float
    waist: float
    hip: float


class IdolDict(TypedDict):
    id: int
    sortId: int
    resourceId: str
    type: int
    fullName: str
    displayName: str
    lastName: str
    firstName: str | None
    alphabetName: str
    fullNameRuby: str
    age: int | None
    height: float
    weight: float
    hobby: str
    specialty: str
    favorites: str
    cv: str
    colorCode: str
    birthplace: MiscDataDict
    handednessType: MiscDataDict
    constellation: MiscDataDict
    bloodType: MiscDataDict
    birthday: BirthdayDict
    measurements: MeasurementsDict
