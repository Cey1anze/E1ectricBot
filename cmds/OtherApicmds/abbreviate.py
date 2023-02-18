import discord
import requests
from discord import app_commands

from Core.init_cog import InitCog

global trans_list, str


def getabbr(text):
    trans_list = []
    trans_list.clear()
    str = ''

    try:
        url = "https://xiaobapi.top/api/xb/api/can_you_speak_in_a_good_way.php?msg={}&type=json".format(text)
        r = requests.get(url)
        result = r.json()

        for item in result:
            trans_list = item['trans']

            for i in range(len(trans_list)):
                str += trans_list[i] + ' , '

        str = str[:-3]

        return str

    except Exception as e:
        return e


class Abbr(InitCog):
    @app_commands.command(name='abbr', description='查询网络缩写的意思')
    @app_commands.describe(text='缩写的文本')
    async def abbr(self, interaction: discord.Interaction, *, text: str):
        await interaction.response.defer()
        await interaction.followup.send(getabbr(text=text))


async def setup(client):
    await client.add_cog(Abbr(client))
