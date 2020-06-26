class Costume(object):
    def __init__(self, data: dict):
        self.id = data['id']
        self.name = data['name']
        self.desc = data['description']
        self.resc_id = data['resourceId']
        self.model_id = data['modelId']
        self.sort_id = data['sortId']

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
        if 'description' in data:
            self.desc = data['description']
        self.type = data['idolType']
        self.spec_type = None
        if 'specificIdolType' in data:
            self.spec_type = data['specificIdolType']
        self.attribute = data['attribute']
        self.value = data['value']

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

class Card(object):
    def __init__(self, data: dict):
        self.id = data['id']
        self.name = data['name']
        self.sort_id = data['sortId']
        self.idol_id = data['idolId']
        self.type = data['idolType']
        self.resc_id = data['resourceId']
        self.rarity = data['rarity']

        self.eventId = data['eventId'] if 'eventId' in data else None

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
