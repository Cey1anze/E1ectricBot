import json


def load_mainconfig():
    with open('./configs/config.json', 'r', encoding='UTF-8') as jf:
        jdata = json.load(jf)
        return jdata


def load_blockwordconfig():
    with open('./configs/blockwords.json', 'r', encoding='UTF-8') as jf:
        keydata = json.load(jf)
        return keydata


def load_replyconfig():
    with open('./configs/replyDict.json', 'r', encoding='UTF-8') as jf:
        replydata = json.load(jf)
        return replydata
