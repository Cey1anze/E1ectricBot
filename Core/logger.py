# 用于记录服务器日志
import time

import discord


def logwrite(msg):
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    with open('./logs/extra_info.log', 'a+', encoding='utf-8') as f:
        f.write('-INFO' + '\t\t' + formatted_time + '\t\t' + msg + '\n')
    f.close()


async def dclogwrite(channel: discord.channel, msg: str):
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    await channel.send(f'{formatted_time} - {msg}')
