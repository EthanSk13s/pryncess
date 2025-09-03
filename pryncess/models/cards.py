from datetime import datetime
from typing import TYPE_CHECKING

import pryncess.models.consts as consts
from pryncess.types.cards import SkillDict

if TYPE_CHECKING:
    from pryncess.types.cards import (
        CostumeDict,
        CenterEffectDict,
        StatsDict,
        ParameterDict,
        StatValues,
        CardDict
    )


class Costume:
    def __init__(self, data: CostumeDict):
        self.id: int = data.get("id")
        self.sort_id: int | None = data.get("sortId")
        self.name: str | None = data.get("name")
        self.desc: str | None = data.get("description")
        self.resc_id: str | None = data.get("resourceId")
        self.model_id: str | None = data.get("modelId")
        self.costume_group_id: int | None = data.get("costumeGroupId")
        self.collab_number: int | None = data.get("collaborationNumber")
        self.default_hairstyle: int | None = data.get("defaultHairstyle")
        self.released_at: datetime | None = data.get("releasedAt")

    def get_image(self):
        img_url = "https://storage.matsurihi.me/mltd/costume_icon_ll"
        image = f"{img_url}/{self.resc_id}.png"

        return image

class BonusCostume(Costume):
    def __init__(self, data: CostumeDict):
        super().__init__(data)


class RankCostume(Costume):
    def __init__(self, data: CostumeDict):
        super().__init__(data)


class CenterEffect:
    def __init__(self, data: CenterEffectDict):
        self.name: str = data.get("name")
        self.id: int = data.get("id")
        self.desc: str | None = data.get("description")
        self.type: int = data.get("idolType")
        self.spec_type: int | None = data.get("specificIdolType")
        self.song_type: int | None = data.get("songType")
        self.attributes: list[int] = data.get("attributes")
        self.values: list[int] = data.get("values")

    def tl_desc(self):
        if self.type != 0:
            if self.desc is not None:
                idol_type = consts.IDOL_TYPES.get(self.type)
                if idol_type is None:
                    idol_type = "Unknown"

                attribute = consts.ATTRIBUTES.get(self.attributes[0])
                value = self.values[0]
                first_cond = consts.CENTER_SKILL_STRING.format(idol_type,
                                                               attribute,
                                                               value)

                if any([idol_type, attribute, first_cond]) is not True:
                    self.desc = "No TL available"
                    return 
                
                if self.id <= 7000:
                    first_cond = consts.CENTER_SKILL_STRING.format(idol_type.capitalize(),
                                                                   attribute,
                                                                   value)
                else:
                    value_2 = self.values[1]
                    first_cond = consts.CENTER_BOOST_STRING.format(value_2,
                                                                   attribute,
                                                                   value)
                if self.song_type is not None:
                    attr_2 = consts.SONG_TYPES.get(self.song_type)
                    value_2 = self.values[1]
                    second_cond = consts.SONG_STRING.format(attr_2)
                    
                    if (self.id % 1000) >= 420 and (self.id % 1000) < 500:
                        third_cond = consts.CENTER_SWING_STRING.format(idol_type.capitalize(),
                                                                       value_2)
                        final_tl = f"{first_cond}. {second_cond} {third_cond}"
                    else:
                        third_cond = consts.CENTER_IDOL_BOOST_STRING.format(value_2)
                        final_tl = f"{first_cond}. {second_cond} {third_cond}"

                    self.desc = final_tl
                else:
                    self.desc = first_cond
        else:
            self.desc = "No Skill."


class Skill:
    def __init__(self, data: SkillDict):
        self.id: int = data.get("id")
        self.desc: str = data.get("description")
        self.effect: int = data.get("effectId")
        self.evaluation_types: list[int] = data.get("evaluations")
        self.values: list[int] = data.get("values")
        self.duration: int = data.get("duration")
        self.interval: int = data.get("interval")
        self.probability: int = data.get("probability")

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
        if self.evaluation_types:
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
        
        effect_str = consts.EFFECTS.get(eff_id)
        if not effect_str:
            self.desc = "No TL available."
            return

        effect_str = effect_str.format(**eff_values)
        self.desc = f"{interval_str} {effect_str} {duration_str}"


class Stats:
    def __init__(self, data: StatsDict):
        self.base: int = data["base"]

        before_awakened = data["beforeAwakened"]
        self.before_awakened: StatValues = StatValues(before_awakened['diff'],
                                                      before_awakened['max'])

        after_awakened = data["afterAwakened"]
        self.after_awakened: StatValues = StatValues(after_awakened['diff'],
                                                     after_awakened['max'])
        self.master_bonus: int = data['masterBonus']


class PartialStats:
    def __init__(self, data: dict[str, int]):
        self.before_awakened: int | None = data["beforeAwakened"]
        self.after_awakened: int | None = data["afterAwakened"]


class Parameters:
    def __init__(self, data: ParameterDict):
        self.vocal: Stats = Stats(data.get("vocal"))
        self.dance: Stats = Stats(data.get("dance"))
        self.visual: Stats = Stats(data['visual'])
        self.lvl_max: PartialStats = PartialStats(data.get("lvMax"))
        self.life: PartialStats = PartialStats(data.get("life"))


class Card:
    def __init__(self, data: CardDict):
        self.id: int = data.get("id")
        self.name: str = data.get("name")
        self.sort_id: int = data.get("sortId")
        self.idol_id: int = data.get("idolId")
        self.type: int = data.get("idolType")
        self.resc_id: str = data.get("resourceId")
        self.rarity: int = data.get("rarity")

        self.ex_type: int = data.get("extraType")
        self.category: int = data.get("category")

        self.max_master_rank: int = data.get("masterRankMax")
        self.max_skill_lvl: int = data.get("skillLvMax")
        self.add_date: datetime = data.get("addedAt")

        prmtrs = data.get("parameters")
        self.parameters: Parameters | None = Parameters(prmtrs) if prmtrs else None

        cntr_skll = data.get("centerEffect")
        self.center_skill: CenterEffect | None = CenterEffect(cntr_skll) if cntr_skll else None

        skills = data.get("skills")
        if skills:
            self.skill: Skill | None = Skill(skills[0])
            self.skill_name: str | None = data.get("skillName")

        costumes = data.get("costumes")
        if costumes:
            default_costume = costumes.get("default")
            bonus_costume = costumes.get("bonus")
            rank_costume = costumes.get("rank5")

            if default_costume:
                self.costume = Costume(default_costume)
            if bonus_costume:
                self.bonus_costume = BonusCostume(bonus_costume)
            if rank_costume:
                self.rank_costume = RankCostume(rank_costume)
        
        # TODO: Add lines for cards

    def get_image(self, img_type: str, bg: bool = False, is_awaken: bool = False) -> str | None:
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
