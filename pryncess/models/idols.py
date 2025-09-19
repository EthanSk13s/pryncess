from pryncess.types.idols import (
    BirthdayDict,
    IdolDict,
    MeasurementsDict,
    MiscDataDict
)


class Birthday:
    """Represents the Birthday of an idol.

    Attributes:
        month (:class:`int`): The birth month.
        day (:class:`int`): The birthday of the birth month.
    """
    def __init__(self, data: BirthdayDict):
        self.month: int = data.get("month")
        self.day: int = data.get("day")
    
    def to_tuple(self) -> tuple[int, int]:
        """Returns the birthday in a tuple.

        Returns:
            tuple[:class:`int`, :class:`int`]: The tuple is formatted as: (`month`, `day`).
        """
        return (self.month, self.day)


class Measurements:
    """Represents the three sizes of an idol.

    Attributes:
        bust (:class:`int`): The bust size of the idol.
        waist (:class:`int`): The waist size of the idol.
        hip (:class:`int`): The hip size of the idol.
    """
    def __init__(self, data: MeasurementsDict):
        self.bust: float = data.get("bust")
        self.waist: float = data.get("waist")
        self.hip: float = data.get("hip")


class MiscData:
    """Represents the miscellaneous data that idols can have.

    Typically, the miscellaneous data will be:
        - Birthplace.
        - Handedness.
        - Birth Constellation.
        - Blood type.

    Attributes:
        id (:class:`int`): The ID of the corresponding data.
        name (:class:`str`): The name of the corresponding data.
    """
    def __init__(self, data: MiscDataDict):
        self.id = data.get("id")
        self.name = data.get("name")


class Idol:
    """Represents an Idol object returned from the Princess API.

    This class is initialized via a TypedDict representing the JSON response
    that the API returns. Therefore, you are not meant to manually initialize
    this class.

    Attributes:
        id (:class:`id`): The ID of the idol.
        sort_id (:class:`int`): The ID that is used when displayed.
        resc_id (:class:`int`): The resource ID used to access various resources.
        type (:class:`int`): The type of the idol. Ranges from 1-5.
        full_name (:class:`str`): The full name of the idol.
        display_name (:class:`str`): The display name of the idol.
        last_name (:class:`str`): The last name of the idol.
        first_name (:class:`str` | `None`): The first name of the idol.
            This will be None for Julia, Shika or Leon.
        alpha_name (:class:`str`): The name of the idol in English.
        full_name_ruby (:class:`str`): The pronounciation for the full name of the idol.
            Will be in Hiragana.
        age (:class:`int` | `None`): The age of the idol. Will be None if the age is unknown.
        birthplace (:class:`MiscData`): The birthplace of the idol.
        handedness (:class:`MiscData`): The handedness of the idol.
        height (:class:`float`): The height of the idol in centimeters.
        weight (:class:`float`): The weight of the idol in kilograms.
        birthday (:class:`Birthday`): The birthday of the idol.
        measurements (:class:`Measurements`): The measurements of the idol.
        constellation (:class:`MiscData`): The birth constellation of the idol.
        blood_type (:class:`MiscData`): The blood type of the idol.
        hobby (:class:`str`): The hobby of the idol. Written in Japanese.
        specialty (:class:`str`): The specialty of the idol. Written in Japanese.
        favorites (:class:`str`): The favorite things of the idol. Written in Japanese.
        cv (:class:`str`): The Voice actress of the idol. Written in Japanese.
        color_code (:class:`str`): The personal color code of the idol in hex form.
    Note:
        When casted to :class:`int`, it will return the ID of the idol.
    """
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
        """Returns the color code of the idol in RGB format.

        Returns:
            tuple[:class:`int`, :class:`int`, :class:`int`]: The color code in RGB format as a tuple.
        """
        hex_str = self.color_code.strip("#")
        r = hex_str[0:2]
        g = hex_str[2:4]
        b = hex_str[4:6]

        return (int(r, 16), int(g, 16), int(b, 16))
    
    def __int__(self):
        return self.id