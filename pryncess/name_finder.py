# -*- coding: utf-8 -*-
""" 
This is used to match names and skills since Princess only has jp strings
Names are from project-imas wiki
Skill descriptions are translated via a machine, and edited to make sense

NOTE: The names indexes are neatly ordered to closely match the idol IDs (Add 1 to index to match)
 However, Extra type idols (e.g: Shika and Leon) have their IDs in the 200s
 So nested dicts with the idol's name and ID is made to make the dict less sensitive
 to sudden changes. 
 Also, another way is to get a card list from API and compare str to id, but its
 a waste of a request.
"""

import re
from .models.cards import Card

names = {
    '天海春香': {'name': 'Amami Haruka', 'id': 1},
    '如月千早': {'name': 'Kisaragi Chihaya', 'id': 2},
    '星井美希': {'name': 'Hoshii Miki', 'id': 3},
    '萩原雪歩': {'name': 'Sugawara Yukiho', 'id': 4},
    '高槻やよい': {'name': 'Takatsuki Yayoi', 'id': 5},
    '菊地真': {'name': 'Kikuchi Makoto', 'id': 6},
    '水瀬伊織': {'name': 'Minase Iori', 'id': 7},
    '四条貴音': {'name': 'Shijou Takane', 'id': 8},
    '秋月律子': {'name': 'Akizuki Ritsuko', 'id': 9},
    '三浦あずさ': {'name': 'Miura Azusa', 'id': 10},
    '双海亜美': {'name': 'Futami Ami', 'id': 11},
    '双海真美': {'name': 'Futami Mami', 'id': 12},
    '我那覇響': {'name': 'Ganaha Hibiki', 'id': 13},
    '春日未来': {'name': 'Kasuga Mirai', 'id': 14},
    '最上静香': {'name': 'Mogami Shizuka', 'id': 15},
    '伊吹翼':  {'name': 'Ibuki Tsubasa', 'id': 16},
    '田中琴葉': {'name': 'Tanaka Kotoha', 'id': 17},
    '島原エレナ': {'name': 'Shimabara Elena', 'id': 18},
    '佐竹美奈子': {'name': 'Satake Minako', 'id': 19},
    '所恵美': {'name': 'Tokoro Megumi', 'id': 20},
    '徳川まつり': {'name': 'Tokugawa Matsuri', 'id': 21},
    '箱崎星梨花': {'name': 'Hakozaki Serika', 'id': 22},
    '野々原茜': {'name': 'Nonohara Akane', 'id': 23},
    '望月杏奈': {'name': 'Mochizuki Anna', 'id': 24},
    'ロコ': {'name': 'Handa Roco', 'id': 25},
    '七尾百合子': {'name': 'Nanao Yuriko', 'id': 26},
    '高山紗代子': {'name': 'Takayama Sayoko', 'id': 27},
    '松田亜利沙': {'name': 'Matsuda Arisa', 'id': 28},
    '高坂海美': {'name': 'Kousaka Umi', 'id': 29},
    '中谷育': {'name': 'Nakatani Iku', 'id': 30},
    '天空橋朋花': {'name': 'Tenkubashi Tomoka', 'id': 31},
    'エミリー': {'name': 'Stewart Emily', 'id': 32},
    '北沢志保': {'name': 'Kitazawa Shiho', 'id': 33},
    '舞浜歩': {'name': 'Maihama Ayumi', 'id': 34},
    '木下ひなた': {'name': 'Kinoshita Hinata', 'id': 35},
    '矢吹可奈': {'name': 'Yabuki Kana', 'id': 36},
    '横山奈緒': {'name': 'Yokoyama Nao', 'id': 37},
    '二階堂千鶴': {'name': 'Nikaido Chizuru', 'id': 38},
    '馬場このみ': {'name': 'Baba Konomi', 'id': 39},
    '大神環': {'name': 'Ogami Tanaka', 'id': 40},
    '豊川風花': {'name': 'Toyokawa Fuka', 'id': 41},
    '宮尾美也': {'name': 'Miyao Miya', 'id': 42},
    '福田のり子': {'name': 'Fukuda Noriko', 'id': 43},
    '真壁瑞希': {'name': 'Makabe Mizuki', 'id': 44},
    '篠宮可憐': {'name': 'Shinomiya Karen', 'id': 45},
    '百瀬莉緒': {'name': 'Momose Rio', 'id': 46},
    '永吉昴': {'name': 'Nagayoshi Subaru', 'id': 47},
    '北上麗花': {'name': 'Kitami Reika', 'id': 48},
    '周防桃子': {'name': 'Suou Momoko', 'id': 49},
    'ジュリア': {'name': 'Julia', 'id': 50},
    '白石紬': {'name': 'Shiraishi Tsumugi', 'id': 51},
    '桜守歌織': {'name': 'Sakuramori Kaori', 'id': 52},
    '詩花': {'name': 'Shika', 'id': 201},
    '玲音': {'name': 'Leon', 'id': 203}
}

skill_descs = {
    1: {'eval1': 'Every {0} seconds, there is a {1}% chance for {2} seconds, to boost Perfect score by {3}%',
    'eval2': 'Every {0} seconds, there is a {1}% chance for {2} seconds, to boost Perfect / Great score by {3}%'},
    2: {'eval1': 'Every {0} seconds, there is a {1}% chance for {2} seconds, to increase Combo Bonus by {3}%'},
    3: {'eval1': 'Every {0} seconds, there is a {1}% chance for {2} seconds, to recover {3} Life for every Perfect'},
    4: {'eval1': 'Every {0} seconds, there is a {1}% chance for {2} seconds, life is not reduced'},
    5: {'eval6': 'Every {0} seconds, there is a {1}% chance for {2} seconds, that every Fast / Slow does not break combo'},
    6: {'eval1': 'Every {0} seconds, there is a {1}% chance for {2} seconds, that Greats becomes Perfect',
    'eval2': 'Every {0} seconds, there is a {1}% chance for {2} seconds, that Greats / Goods becomes Perfect',
    'eval7': 'Every {0} seconds, there is a {1}% chance for {2} seconds, that Greats / Goods / Fast / Slow becomes Perfect'},
    7: {'eval1': 'Every {0} seconds there is a {1}% chance for {2} seconds, boosts Perfect score by {3}%, and combo bonus by {4}%'},
    8: {'eval2': 'Every {0} seconds there is a {0}% chance of consuming {1} lives, and for {2} seconds, Perfect score will increase by {3}%'},
    10: {'eval2': 'Every {0} seconds there is a {0}% chance of consuming {1} lives, and for {2} seconds, Perfect / Great score will increase by {3}%'}
}

def match_name(query: str):
    if query in names:
        return names.get(query)['name']

def match_id(query: str):
    if query in names:
        return names.get(query)['id']
    else:        
        for values in names.values():
            regex = r"\b{0}\b".format(query.lower())
            match = bool(re.search(regex, values['name'].lower()))
            if match:
                return values['id']

def set_name(card: 'Card'):
    if '　' in card.name:
        title, name = card.name.split('　')
        new_name = match_name(name)
        card.name = f"{title} {new_name}"
    else:
        new_name = match_name(card.name)
        card.name = new_name

def set_desc(card: 'Card'):
    desc = skill_descs.get(card.skill.effect)
    if  7 > card.skill.effect >= 4:
        if card.skill.evaluation > 1:
            new_desc = desc[f'eval{card.skill.evaluation}'].format(card.skill.interval,
            card.skill.probability, card.skill.duration)
        else:
            new_desc = desc['eval1'].format(card.skill.interval,
            card.skill.probability, card.skill.duration)

    elif card.skill.effect == 7:
        new_desc = desc[f'eval{card.skill.evaluation}'].format(card.skill.interval,
        card.skill.probability, card.skill.duration, card.skill.value[0], card.skill.value[1])

    else:
        if card.skill.evaluation > 1:
            new_desc = desc[f'eval{card.skill.evaluation}'].format(card.skill.interval,
            card.skill.probability, card.skill.duration, card.skill.value[0])
        else:
            new_desc = desc['eval1'].format(card.skill.interval,
            card.skill.probability, card.skill.duration, card.skill.value[0])
    
    card.skill.desc = new_desc