# coding:utf-8
from aliyunsdkcore.client import AcsClient
from aliyunsdkalimt.request.v20181012 import TranslateGeneralRequest

import json
import langid
import discord
import pyperclip as pc
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
)

Private = False
isPrivate = '公开'


# 获取翻译结果
def get_translate(text: str):
    try:
        request = TranslateGeneralRequest.TranslateGeneralRequest()
        request.set_SourceLanguage(langid.classify(text)[0])
        request.set_SourceText(text)
        request.set_FormatType("text")
        request.set_TargetLanguage(lang)
        request.set_method("POST")
        # 发起API请求并显示返回值
        response = client.do_action_with_exception(request)
        return json.loads(response)['Data']['Translated']
    except Exception as e:
        return e


# 创建嵌入式消息
def create_embed(text):
    judge = get_translate(text)
    line = '-' * 12
    if not isinstance(judge, Exception):
        embed = discord.Embed(title="翻译结果", description=f'已切换显示模式为 : {isPrivate} ,如需切换显示模式，请点击下方按钮', color=0x00ff00)
        embed.add_field(name=f'{line}原文{line}', value=text, inline=False)
        embed.add_field(name=f'{line}译文{line}', value=f'{get_translate(text)}', inline=False)
        embed.set_footer(text='Translate engine powered by Aliyun')
        return embed
    else:
        embed = discord.Embed(title="请求失败", description=f'{Exception}', color=0xDC143C)
        return embed


class Buttons(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.copy = discord.ui.Button(label="复制译文", style=discord.ButtonStyle.green)
        self.private = discord.ui.Button(label="仅自己", style=discord.ButtonStyle.red)
        self.pubilc = discord.ui.Button(label="公开", style=discord.ButtonStyle.green)
        self.dm = discord.ui.Button(label="私信", style=discord.ButtonStyle.green)
        # self.add_item(self.copy)  如果你的机器人在本地运行，那么你可以取消注释，会恢复复制译文的按钮，用来复制译文到系统剪切板
        self.add_item(self.pubilc)
        self.add_item(self.private)
        self.add_item(self.dm)
        self.copy.callback = copy_translate
        self.private.callback = private_message
        self.pubilc.callback = public_message
        self.dm.callback = direct_message


# callback
async def copy_translate(interaction: discord.Interaction):
    pc.copy(result)
    await interaction.response.send_message("已复制译文到剪切板", ephemeral=True)


async def private_message(interaction: discord.Interaction):
    global Private, isPrivate
    if interaction.user == user:
        isPrivate = '仅自己'
        returnedembed = create_embed(t)
        await interaction.response.edit_message(embed=returnedembed)
        if not Private:
            Private = not Private
            await interaction.followup.send(
                "> **Info: 接下来，`/translate`的返回结果仅您自己可见。如想让所有人看到返回结果，请点击`公开`**", ephemeral=True)
        else:
            await interaction.followup.send(
                "> **Warn: 你已经设置过仅自己可见，如想让所有人看到返回结果，请点击`公开`**", ephemeral=True)
    else:
        await interaction.response.send_message("你没有权限点击其他用户的交互按钮", ephemeral=True)


async def public_message(interaction: discord.Interaction):
    global Private, isPrivate
    if interaction.user == user:
        isPrivate = '公开'
        returnedembed = create_embed(t)
        await interaction.response.edit_message(embed=returnedembed)
        if Private:
            Private = not Private
            await interaction.followup.send(
                "> **Info: 接下来，`/translate`的返回结果可以被所以人看见。如需仅自己可见，请点击`仅自己`**", ephemeral=True)
        else:
            await interaction.followup.send(
                "> **Warn: 你已经设置过所有人可见，如需仅自己可见，请点击`仅自己`**", ephemeral=True)
    else:
        await interaction.response.send_message("你没有权限点击其他用户的交互按钮", ephemeral=True)


async def direct_message(interaction: discord.Interaction):
    await interaction.response.defer()
    await interaction.user.send("哈喽，接下来你可以直接在私信中使用`/translate`或其他指令")
    await interaction.followup.send("请检查你的私信", ephemeral=True)


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
        global lang, result, t, user
        t = text
        user = interaction.user
        await interaction.response.defer(ephemeral=Private)
        lang_options = {0: "zh", 1: "en", 2: "fr", 3: "de", 4: "ru", 5: "ja"}
        lang = lang_options.get(option)
        result = get_translate(text)
        await interaction.followup.send(embed=create_embed(text), view=Buttons())

        ''''
        stupid way(直白但不够模块化,可读性很差) ↓
        
        copy = Button(label="复制译文", style=discord.ButtonStyle.green)
        view = discord.ui.View()
        view.add_item(copy)
        copy.callback = self.copy_translate
        await interaction.followup.send(embed=create_embed(text), view=view)

    async def copy_translate(self, interaction: discord.Interaction):
        pc.copy(result)
        await interaction.response.send_message("已复制译文到剪切板", ephemeral=True)
        '''


async def setup(client):
    await client.add_cog(Translate(client))
