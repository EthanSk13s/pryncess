import typing

# TODO: Maybe add a utility function to return a tuple for month and day
class Birthday:
    def __init__(self, data: dict):
        self.month: int = data['month']
        self.day: int = data['day']

class Measurements:
    def __init__(self, data: dict):
        self.bust: float = data['bust']
        self.waist: float = data['waist']
        self.hip: float = data['hip']

class Idol:
    def __init__(self, data: dict):
        misc_data = typing.NamedTuple('MiscData', [('id', int), ('name', str)])

        self.id: int = data['id']
        self.sort_id: int = data['sortId']
        self.resc_id: str = data['resourceId']
        self.type: int = data['type']

        self.full_name: str = data['fullName']
        self.display_name: str = data['displayName']
        self.last_name: str = data['lastName']
        self.first_name: typing.Union[str, None] = data['firstName']
        self.alpha_name: str = data['alphabetName']
        self.full_name_ruby: str = data['fullNameRuby']

        self.age: typing.Union[int, None] = data['age']
        self.birthplace = misc_data(data['birthplace'])
        self.handedness = misc_data(data['handednessType'])

        self.height: int = data['height']
        self.weight: int = data['weight']
        self.birthday: Birthday = Birthday(data['birthday'])
        self.measurements: Measurements = Measurements(data['measurements'])

        self.hobby: str = data['hobby']
        self.specialty: str = data['specialty']
        self.favorites: str = data['favorites']

        self.cv: str = data['cv']
        self.color_code: str = data['colorCode']
        self.constellation = misc_data(data['constellation'])
        self.blood_type = misc_data(data['bloodType'])