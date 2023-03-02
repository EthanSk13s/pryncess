import typing

import pryncess.models.consts as consts

class Costume(object):
    def __init__(self, data: dict):
        self.id: int = data['id']
        self.sort_id: typing.Union[int, None] = data['sortId'] if 'sortId' in data else None
        self.name: typing.Union[str, None] = data['name'] if 'name' in data else None
        self.desc: typing.Union[str, None] = data['description'] if 'description' in data else None
        self.resc_id: typing.Union[str, None] = data['resourceId'] if 'resourceId' in data else None
        self.model_id: typing.Union[str, None] = data['modelId'] if 'modelId' in data else None
        self.costume_group_id: typing.Union[int, None] = data['costumeGroupId'] if 'costumeGroupId' in data else None
        self.collab_number: typing.Union[int, None] = data['collaborationNumber'] if 'collaborationNumber' in data else None
        self.default_hairstyle: typing.Union[int, None] = data['defaultHairstyle'] if 'defaultHairstyle' in data else None
        self.released_at = data['releasedAt'] if 'releasedAt' in data else None 

    def get_image(self):
        img_url = "https://storage.matsurihi.me/mltd/costume_icon_ll"
        image = f"{img_url}/{self.resc_id}.png"

        return image

class BonusCostume(Costume):
    def __init__(self, data: dict):
        super().__init__(data)


class RankCostume(Costume):
    def __init__(self, data: dict):
        super().__init__(data)


class CenterEffect(object):
    def __init__(self, data: dict):
        self.name: str = data['name']
        self.id: int = data['id']
        self.desc: typing.Union[str, None] = data['description'] if 'description' in data else None
        self.type: int = data['idolType']
        self.spec_type: typing.Union[int, None] = data['specificIdolType'] if 'specificIdolType' in data else None
        self.song_type: typing.Union[int, None] = data['songType'] if 'songType' in data else None
        self.attributes: list[int] = data['attributes']
        self.values: list[int] = data['values']

    def tl_desc(self):
        if self.type != 0:
            if self.desc is not None:
                idol_type = consts.IDOL_TYPES.get(self.type)
                attribute = consts.ATTRIBUTES.get(self.attributes[0])
                value = self.values[0]
                first_cond = consts.CENTER_SKILL_STRING.format(idol_type,
                                                               attribute,
                                                               value)

                if any([idol_type, attribute, first_cond]) is None:
                    self.desc = "No TL available"
                    return 
                
                if self.id <= 7000:
                    first_cond = consts.CENTER_SKILL_STRING.format(
                                                                   idol_type.capitalize(),
                                                                   attribute,
                                                                   value)
                else:
                    value_2 = self.values[1]
                    first_cond = consts.CENTER_BOOST_STRING.format(value_2,
                                                            attribute,
                                                            value)
                if self.song_type != 0:
                    attr_2 = consts.SONG_TYPES.get(self.song_type)
                    value_2 = self.values[1]
                    second_cond = consts.SONG_STRING.format(attr_2, value_2)
                    final_tl = f"{first_cond}. {second_cond}"
                    self.desc = final_tl
                else:
                    self.desc = first_cond
            else:
                pass
        else:
            self.desc = "No Skill."


class Skill(object):
    def __init__(self, data: dict):
        self.id: int = data['id']
        self.desc: str = data['description']
        self.effect: int = data['effectId']
        self.evaluation_types: list[int] = data['evaluationTypes']
        self.values: list[int] = data['values']
        self.duration: int = data['duration']
        self.interval: int = data['interval']
        self.probability: int = data['probability']

    def tl_desc(self):
        interval = self.interval
        probability = self.probability
        duration = self.duration

        interval_str = consts.INTERVAL_STRING.format(interval=interval,
                                              probability=probability)
        duration_str = consts.DURATION_STRING.format(duration=duration)

        eff_id = self.effect
        # Does not need any modification, so we just get the effect string
        if eff_id == 4:
            skill_string = f"{interval_str} {consts.EFFECTS.get(eff_id)} {duration_str}"
            self.desc = skill_string
            return

        eff_values = {}
        if self.evaluation_types is not None:
            eval_types = self.evaluation_types
            eval_size: int = len(self.evaluation_types)
            if eval_size == 1:
                eff_values['evaluation'] = consts.EVALUATIONS.get(eval_types[0])

            if eval_size == 2:
                eff_values['evaluation2'] = consts.EVALUATIONS.get(eval_types[1])

            if eval_size == 3:
                eff_values['evaluation3'] = consts.EVALUATIONS.get(eval_types[2])

        if len(self.values) != 0:
            eff_values['value'] = self.values
        try:
            effect_str = consts.EFFECTS.get(eff_id).format(**eff_values)
        except AttributeError:
            self.desc = "No TL available"
            return

        self.desc = f"{interval_str} {effect_str} {duration_str}"

class Stats(object):
    def __init__(self, data: dict):
        stat_values = typing.NamedTuple('StatValues', [('diff', int), ('max', int)])
        self.base: int = data['base']

        before_awakened = data['beforeAwakened']
        self.before_awakened = stat_values(before_awakened['diff'],
                                           before_awakened['max'])

        after_awakened = data['afterAwakened']
        self.after_awakened = stat_values(after_awakened['diff'], after_awakened['max'])
        self.master_bonus: int = data['masterBonus']

class PartialStats(object):
    def __init__(self, data: dict):
        self.before_awakened: int = data['beforeAwakened']
        self.after_awakened: int = data['afterAwakened']

class Parameters(object):
    def __init__(self, data: dict):
        self.vocal: Stats = Stats(data['vocal'])
        self.dance: Stats = Stats(data['dance'])
        self.visual: Stats = Stats(data['visual'])
        self.lvl_max: PartialStats = PartialStats(data['lvMax'])
        self.life: PartialStats = PartialStats(data['life'])

class Card(object):
    def __init__(self, data: dict):
        self.id: int = data['id']
        self.name: str = data['name']
        self.sort_id: int = data['sortId']
        self.idol_id: int = data['idolId']
        self.type: int = data['idolType']
        self.resc_id: str = data['resourceId']
        self.rarity: str = data['rarity']

        self.ex_type: int = data['extraType'] if 'extraType' in data else None
        # TODO: add category attribute

        self.max_master_rank: int = data['masterRankMax']
        self.max_skill_lvl: int = data['skillLvMax']
        self.add_date = data['addDate'] if 'addDate' in data else None
        self.costume: typing.Union[Costume, None] = None
        self.bonus_costume: typing.Union[Costume, None] = None
        self.rank_costume: typing.Union[Costume, None] = None
        self.parameters: typing.Union[Parameters, None] = None
        self.center_skill: typing.Union[CenterEffect, None] = None
        self.skill_name: typing.Union[str, None] = None
        self.skill = Skill(data['skills'][0]) if 'skills' in data else None

        costumes = data['costumes']
        if 'default' in costumes:
            self.costume = Costume(costumes['default'])

        if 'bonus' in costumes:
            self.bonus_costume = BonusCostume(costumes['bonus'])

        if 'rank5' in costumes:
            self.rank_costume = RankCostume(costumes['rank5'])

        # TODO: Fix flavor texts, its wrapped in lines in JSON data
        if 'flavorText' in data:
            self.flavor = data['flavorText']
            self.awake_flavor = data['flavorTextAwakened']
        else:
            self.flavor = None
            self.awake_flavor = None

        if 'parameters' in data:
            self.parameters = Parameters(data['parameters'])

        if 'centerEffect' in data:
            self.center_skill = CenterEffect(data['centerEffect'])

        if self.skill is not None:
            self.skill_name = data['skillName'] if 'skillName' in data else None

    def get_image(self, img_type: str, bg=False, is_awaken=False) -> str:
        img_path = "https://storage.matsurihi.me/mltd"
        int_awk = int(is_awaken)

        # Convert bool to string for url equivalence of True/False
        if bg:
            str_bg = 'b'
        else:
            str_bg = 'a'

        img_types = {
                "card": f"{img_path}/card/{self.resc_id}_{int_awk}_{str_bg}.png",
                "icon": f"{img_path}/icon_l/{self.resc_id}_{int_awk}.png"
                }

        if self.rarity == 4:
            img_types['card_bg'] = f"{img_path}/card_bg/{self.resc_id}_{int_awk}.png"

        image = img_types.get(img_type)

        return image
