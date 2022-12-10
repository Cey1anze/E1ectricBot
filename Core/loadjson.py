import json


def load_mainconfig():
    with open('./config.json', 'r', encoding='UTF-8') as jf:
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


def load_channelconfig():
    with open('./configs/channel.json', 'r', encoding='UTF-8') as jf:
        channeldata = json.load(jf)
        return channeldata


def load_roleconfig():
    with open('./configs/roles.json', 'r', encoding='UTF-8') as jf:
        roledata = json.load(jf)
        return roledata


def load_helpconfig():
    with open('./configs/help.json', 'r', encoding='UTF-8') as jf:
        helpembed = json.load(jf)
        return helpembed


def load_chatconfig():
    with open('./configs/chatGPT.json', 'r', encoding='UTF-8') as jf:
        chatbot = json.load(jf)
        return chatbot
