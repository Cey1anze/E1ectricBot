import discord
import requests
from discord import app_commands

from Core.init_cog import InitCog


def getimg(tag):
    try:
        url = "https://pixiv-ab.tk/api/pixiv/daily/tag/{}".format(tag)
        r = requests.get(url)
        result = r.json()
        url = result['url']
        title = result['title']
        artist = result['artist']
        id = result['id']

        embed = discord.Embed()
        embed.add_field(name="作品标题", value=f'{title}', inline=True)
        embed.add_field(name="作者", value=f'{artist}', inline=True)
        embed.add_field(name="作品ID", value=f'{id}', inline=True)
        embed.set_image(url=url)

        return embed

    except Exception as e:
        return discord.Embed(title="出错了", description=f"{e}", colour=discord.Color.red())


class Pixiv(InitCog):
    @app_commands.command(name='pixiv-image', description='随机Pixiv图片')
    @app_commands.describe(tag='关键字，可以是多个')
    async def genshinimg(self, interaction: discord.Interaction, *, tag: str):
        await interaction.response.defer()
        embed = getimg(tag)
        await interaction.followup.send(embed=embed)


async def setup(client):
    await client.add_cog(Pixiv(client))
