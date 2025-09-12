from pryncess.types.idols import (
    BirthdayDict,
    IdolDict,
    MeasurementsDict,
    MiscDataDict
)


class Birthday:
    def __init__(self, data: BirthdayDict):
        self.month: int = data.get("month")
        self.day: int = data.get("day")
    
    def to_tuple(self) -> tuple[int, int]:
        return (self.month, self.day)


class Measurements:
    def __init__(self, data: MeasurementsDict):
        self.bust: float = data.get("bust")
        self.waist: float = data.get("waist")
        self.hip: float = data.get("hip")


class MiscData:
    def __init__(self, data: MiscDataDict):
        self.id = data.get("id")
        self.name = data.get("name")


class Idol:
    def __init__(self, data: IdolDict):
        self.id: int = data.get("id")
        self.sort_id: int = data.get("sortId")
        self.resc_id: str = data.get("resourceId")
        self.type: int = data.get("type")

        self.full_name: str = data.get("fullName")
        self.display_name: str = data.get("displayName")
        self.last_name: str = data.get("lastName")
        self.first_name: str | None = data.get("firstName")
        self.alpha_name: str = data.get("alphabetName")
        self.full_name_ruby: str = data.get("fullNameRuby")

        self.age: int | None = data.get("age")
        self.birthplace = MiscData(data.get("birthplace"))
        self.handedness = MiscData(data.get("handedness"))

        self.height: float = data.get("height")
        self.weight: float = data.get("weight")

        self.birthday: Birthday = Birthday(data.get("birthday"))
        self.measurements: Measurements = Measurements(data.get("measurements"))
        self.constellation = MiscData(data.get("constellation"))
        self.blood_type = MiscData(data.get("bloodType"))

        self.hobby: str = data.get("hobby")
        self.specialty: str = data.get("specialty")
        self.favorites: str = data.get("favorites")

        self.cv: str = data.get("cv")
        self.color_code: str = data.get("colorCode")

    def color_code_to_rgb(self)-> tuple[int, int, int]:
        hex_str = self.color_code.strip("#")
        r = hex_str[0:2]
        g = hex_str[2:4]
        b = hex_str[4:6]

        return (int(r, 16), int(g, 16), int(b, 16))
    
    def __int__(self):
        return self.id