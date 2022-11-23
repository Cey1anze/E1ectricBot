import json


def load():
    with open('./config.json', 'r', encoding='UTF-8') as jf:
        jdata = json.load(jf)
        return jdata
