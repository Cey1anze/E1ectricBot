# coding:utf-8
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalimt.request.v20181012 import TranslateGeneralRequest

import json
import langid
import discord
from discord import app_commands
from discord.app_commands import Choice

from Core.init_cog import InitCog
from Core.loadjson import load_transconfig

config = load_transconfig()

# 创建AcsClient实例
client = AcsClient(
    config['id'],  # 阿里云账号的AccessKey ID
    config['secret'],  # 阿里云账号Access Key Secret
    config['area']  # 地域ID
);


class Translate(InitCog):

    @app_commands.command(name='translate', description='翻译文本')
    @app_commands.describe(text='需要翻译的内容')
    @app_commands.rename(option='需要翻译成什么语言')
    @app_commands.choices(option=[
        Choice(name='汉语', value=0),
        Choice(name='英语', value=1),
        Choice(name='法语', value=2),
        Choice(name='德语', value=3),
        Choice(name='俄语', value=4),
        Choice(name='日语', value=5)
    ])
    async def translate(self, interaction: discord.Interaction, text: str, option: int):
        global lang
        await interaction.response.defer()
        if option == 0:
            lang = "zh"
        if option == 1:
            lang = "en"
        if option == 2:
            lang = "fr"
        if option == 3:
            lang = "de"
        if option == 4:
            lang = "ru"
        if option == 5:
            lang = "ja"
        try:
            # 创建request，并设置参数
            request = TranslateGeneralRequest.TranslateGeneralRequest()
            request.set_SourceLanguage(langid.classify(text)[0])
            request.set_SourceText(text)
            request.set_FormatType("text")
            request.set_TargetLanguage(lang)
            request.set_method("POST")
            # 发起API请求并显示返回值
            response = client.do_action_with_exception(request)
            result = json.loads(response)['Data']['Translated']
            await interaction.followup.send(embed=
                                            discord.Embed(title='翻译结果：', description=f'{result}',
                                                          colour=discord.Color.from_rgb(130, 156, 242)))
        except Exception as e:
            print(e)
            await interaction.followup.send(e)


async def setup(client):
    await client.add_cog(Translate(client))
