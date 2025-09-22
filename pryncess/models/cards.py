from datetime import datetime

import pryncess.models.consts as consts
from pryncess.types.cards import (
    CostumeDict,
    CenterEffectDict,
    StatsDict,
    SkillDict,
    ParameterDict,
    StatValues,
    CardDict
)


class Costume:
    """Represents the costume of a card.

    This class is composed with a Card object. Like other composed
    objects for the card, it is not meant to be manually initialized.

    Attributes:
        id (:class:`int`): ID of the costume.
        sort_id (:class:`int` | `None`): ID used for sorting when displayed.
        name (:class:`str` | `None`): Name of the costume.
        desc (:class:`str` | `None`): Description of the costume.
        resc_id (:class:`str` | `None`): ID used to access resources.
        model_id (:class:`str` | `None`): ID used for the 3D Model.
        costume_group_id (:class:`int` | `None`): ID of the costume group.
            This will be None if the costume is for overseas version.
        collab_number (:class:`int` | `None`): ID of the texture of the costume with texture variations.
        default_hairstyle (:class:`int` | `None`): ID of the default hairstyle.
            This will be None if the costume is for overseas version.
        released_at (:class:`datetime.datetime` | `None`): Date when the costume is added. 
    """
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
    """Represents the Bonus Costume of a card. Subclass of Costume.
    """
    def __init__(self, data: CostumeDict):
        super().__init__(data)


class RankCostume(Costume):
    """Represents the Rank Costume of a card. Subclass of Costume.
    """
    def __init__(self, data: CostumeDict):
        super().__init__(data)


class CenterEffect:
    """Represents the Center Skill or effect of a card.

    This class is composed with a Card object. Like other composed
    objects for the card, it is not meant to be manually initialized.
    Similar to the Skill class, this class can be English translated.

    Attributes:
        name (:class:`str`): Name of the Center Effect.
        id (:class:`int`): ID of the Center Effect.
        description (:class:`str` | `None`): Description of the Center Effect.
        type (:class:`int`): The idol type that the Center Effect would be applied to.
        spec_type (:class:`int` | `None`): The idol type that all idols in a unit should have when the Center Effect is applied.
        song_type (:class:`int` | `None`): The song type that the center effect requires to be able to apply.
        attributes (list[:class:`int`]): Parameters that the center effect will be applied to. Ranges from 1-8.
        values (list[:class:`int`]): Values of the center effect in percentage.
    """
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
        """Translates the description of the skill to English.

        Translates the skill description to English using the ID and
        using the template descrition of the raw string. Note: The template
        string will be lost in the process as it will be replaced with the
        English translation.
        """
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
    """Represents the skill associated with a card.

    This class is composed with a Card object. Like other composed
    objects for the card, it is not meant to be manually initialized.

    Attributes:
        id (:class:`int`): Skill ID for the skill.
        desc (:class:`str`): Template description for the skill.
            If the skill is translated, it will be the English description.
        effect (:class:`int`): Effect ID of the skill, ranges from 1-18.
            Representing the different effects that the skill can do.
        evaluation_types (list[:class:`int`]): Conditions that the skill needs to activate. Ranges from 0-7.
        values (list[:class:`int`]): Values of the skill effect.
        duration (:class:`int`): Duration of the skill in seconds.
        interval (:class:`int`): Interval of when the skill activates in seconds.
        probability (:class:`int`): Chance of the skill activating in percentage.
    """
    def __init__(self, data: SkillDict):
        self.id: int = data.get("id")
        self.desc: str = data.get("description")
        self.effect: int = data.get("effectId")
        self.evaluation_types: list[int] = data.get("evaluationTypes")
        self.values: list[int] = data.get("values")
        self.duration: int = data.get("duration")
        self.interval: int = data.get("interval")
        self.probability: int = data.get("probability")

    def tl_desc(self):
        """Translates the description of the skill to English.

        Translates the skill description to English using the effect ID and
        using the template descrition of the raw string. Note: The template
        string will be lost in the process as it will be replaced with the
        English translation.
        """
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
    """Represents the various values of a stat and specific values for calculating
    values at different levels.

    Attributes:
        base (:class:`int`): Value of the stat at Level 1.
        before_awakened (:class:`StatValues`): Initial incremental values of the stat.
        after_awakened (:class:`StatValues`): Awakened incremental values of the stat.
        master_bonus (:class:`StatValues`): Bonus value per master rank.
    """
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
    """Represent the values of a stat for the initial state of a card, and
    when it's awakened.

    The difference between this class and the Stats class is that it only
    contains values when the card is in its initial state or its awakened state.

    Attributes:
        before_awakened (:class:`int` | None): Value of a stat before it is awakened.
        after_awakened (:class:`int` | None): Value of a stat after it is awakened.
    """
    def __init__(self, data: dict[str, int]):
        self.before_awakened: int | None = data["beforeAwakened"]
        self.after_awakened: int | None = data["afterAwakened"]


class Parameters:
    """Represents the various stats a card will have.

    This class is not to be manually initialized and is composed via a Card object.
    This class represents the various numerical stats that card will have.
    These include: Vocal, Dance, Visual, the max level, and the life of a
    specific card.

    Attributes:
        vocal (:class:`Stats`): Vocal stats of the card.
        dance (:class:`Stats`): Dance stats of the card.
        visual (:class:`Stats`): Visual stats of the card.
        lvl_max (:class:`PartialStats`): Max level of the card.
        life (:class:`PartialStats`): Life values of the card.
    """
    def __init__(self, data: ParameterDict):
        self.vocal: Stats = Stats(data.get("vocal"))
        self.dance: Stats = Stats(data.get("dance"))
        self.visual: Stats = Stats(data['visual'])
        self.lvl_max: PartialStats = PartialStats(data.get("lvMax"))
        self.life: PartialStats = PartialStats(data.get("life"))


class Card:
    """Represents a card object from the response Princess returns.

    This class is initialized via a TypedDict representing the JSON response
    that the API returns. Therefore, you are not meant to manually initialize
    this class. Refer to Princess API documentation for more details for what
    each attribute means. Especially that of integer types.

    Attributes:
        id (:class:`int`): ID for the card.
        name (:class:`str`): The card's name. This can be a translated string or just the raw string.
        sort_id (:class:`int`): Sort ID that is used when displayed.
        idol_id (:class:`int`): ID for the idol that the card belongs to.
        type (:class:`int`): Type of the idol's attribute.
        resc_id (:class:`str`): Resource ID for images and assets.
        rarity (:class:`int`): Rarity level of the card ranging from 1-4.
        ex_type (:class:`int`): Extra type of the card ranging from 0-22 (excluding 1).
        category (:class:`int`): Category of the card.
        max_master_rank (:class:`int`): Maximum master rank.
        max_skill_lvl (:class:`int`): Maximum skill level.
        add_date (:class:`datetime.datetime`): Date when the card was added to the game.
        parameters (:class:`Parameters` | `None`): Card parameters.
        center_skill (:class:`CenterEffect` | `None`): Center Skill associated with the card.
        skill (:class:`Skill` | None): Skill associated to the card.
        skill_name (:class:`str` | `None`): Name of the card's skill.
        costume (:class:`Costume` | `None`): Default costume unlocked by the card.
        bonus_costume (:class:`BonusCostume` | `None`): Bonus costume tied to the card.
        rank_costume (:class:`RankCostume` | `None`): Rank 5 costume tied to the card.
    """
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
        else:
            self.skill = None
            self.skill_name = None

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
        """Returns the URL for a card's image.

        Constructs the appropriate image URL based on the card's resource ID,
        image type, background flag, and whether the image is the awakened version.

        Args:
            img_type (:class:`str`): The type of image to retrieve. Supported values:
                - "card": Full-size card image.
                - "icon": Icon-sized card image.
                - "card_bg": Background image for 4-star rarity cards.
            bg (:class:`bool`, optional): Whether to fetch the "background" version of
                the card image. Defaults to False.
            is_awaken (:class:`bool`, optional): Whether to fetch the awakened version
                of the image. Defaults to False.

        Returns:
            :class:`str` | `None`: The URL string of the requested image, or None if the
            `img_type` is unsupported for this card.
        """

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
