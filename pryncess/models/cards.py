from .consts import *

class Costume(object):
    def __init__(self, data: dict):
        self.id = data['id']
        self.name = data['name']
        self.desc = data['description']
        self.resc_id = data['resourceId']
        self.model_id = data['modelId']
        self.sort_id = data['sortId']

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
        self.id = data['id']
        self.desc = None
        self.desc = data['description'] if 'description' in data else None
        self.type = data['idolType']
        self.spec_type = data['specificIdolType'] if 'specificIdolType' in data else None
        self.song_type = data['songType'] if 'songType' in data else None
        self.attribute = data['attribute']
        self.attribtue_2 = data['attribute2'] if 'attribute2' in data else None
        self.value = data['value']
        self.value_2 = data['value2'] if 'value2' in data else None

    def tl_desc(self):
        if self.desc is not None:
            idol_type = IDOL_TYPES.get(self.type)
            attribute = ATTRIBUTES.get(self.attribute)
            value = self.value
            first_cond = CENTER_SKILL_STRING.format(idol_type, attribute, value)

            if any(idol_type, attribute, first_cond) is None:
                self.desc = "No TL available"
                return 

            if self.song_type is not None:
                attr_2 = SONG_TYPES.get(self.song_type)
                value_2 = self.value_2
                second_cond = SONG_STRING.format(attr_2, value_2)
                final_tl = f"{first_cond}. {second_cond}"
                self.desc = final_tl
            else:
                self.desc = first_cond
        else:
            pass


class Skill(object):
    def __init__(self, data: dict):
        self.id = data['id']
        self.desc = data['description']
        self.effect = data['effectId']
        self.evaluation = data['evaluation']
        self.evaluation2 = data['evaluation2']
        self.duration = data['duration']
        self.interval = data['interval']
        self.probability = data['probability']
        self.value = data['value']

    def tl_desc(self):
        interval = self.interval
        probability = self.probability
        duration = self.duration

        interval_str = INTERVAL_STRING.format(interval=interval,
                                              probability=probability)
        duration_str = DURATION_STRING.format(duration=duration)

        eff_id = self.effect
        # Does not need any modification, so we just get the effect string
        if eff_id == 4:
            skill_string = f"{interval_str} {EFFECTS.get(eff_id)} {duration_str}"
            self.desc = skill_string
            return

        eff_values = {}
        if self.evaluation != 0:
            eff_values['evaluation'] = EVALUATIONS.get(self.evaluation)

        if len(self.value) != 0:
            eff_values['value'] = self.value

        if self.evaluation2 != 0:
            eff_values['evaluation2'] = EVALUATIONS.get(self.evaluation2)

        try:
            effect_str = EFFECTS.get(eff_id).format(**eff_values)
        except AttributeError:
            self.desc = "No TL available"
            return

        self.desc = f"{interval_str} {effect_str} {duration_str}"


class Card(object):
    def __init__(self, data: dict):
        self.id = data['id']
        self.name = data['name']
        self.sort_id = data['sortId']
        self.idol_id = data['idolId']
        self.type = data['idolType']
        self.resc_id = data['resourceId']
        self.rarity = data['rarity']

        self.event_id = data['eventId'] if 'eventId' in data else None

        self.ex_type = data['extraType']

        self.costume = Costume(data['costume']) if 'costume' in data else None

        if 'bonusCostume' in data:
            self.bonus_costume = BonusCostume(data['bonusCostume'])
        else:
            self.bonus_costume = None

        if 'rank5Costume' in data:
            self.rank_costume = RankCostume(data['rank5Costume'])
        else:
            self.rank_costume = None
        if 'flavorText' in data:
            self.flavor = data['flavorText']
            self.awake_flavor = data['flavorTextAwakened']
        else:
            self.flavor = None
            self.awake_flavor = None

        self.max_level = data['levelMax']
        self.max_awake_level = data['levelMaxAwakened']

        self.min_vocal = data['vocalMin']
        self.max_vocal = data['vocalMax']
        self.min_awake_vocal = data['vocalMinAwakened']
        self.max_awake_vocal = data['vocalMaxAwakened']
        self.bonus_vocal = data['vocalMasterBonus']

        self.min_dance = data['danceMin']
        self.max_dance = data['danceMax']
        self.min_awake_dance = data['danceMinAwakened']
        self.max_awake_dance = data['danceMaxAwakened']
        self.bonus_dance = data['danceMasterBonus']

        self.min_visual = data['visualMin']
        self.max_visual = data['visualMax']
        self.min_awake_visual = data['visualMinAwakened']
        self.max_awake_visual = data['visualMaxAwakened']
        self.bonus_visual = data['visualMasterBonus']

        self.life = data['life']

        if 'centerEffect' in data:
            self.center_skill = CenterEffect(data['centerEffect'])
        else:
            self.center_skill = None

        if self.center_skill is None:
            self.center_name = data['centerEffectName']

        self.skill = Skill(data['skill'][0]) if 'skill' in data else None

        if self.skill is not None:
            self.skill_name = data['skillName']
        else:
            self.skill_name = None

        self.add_date = data['addDate'] if 'addDate' in data else None

    def get_image(self, img_type: str, bg=False, is_awaken=False):
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
