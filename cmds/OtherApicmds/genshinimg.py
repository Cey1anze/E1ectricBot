import discord
import requests
from discord import app_commands

from Core.init_cog import InitCog


def getimg():
    try:
        url = "http://api.starrobotwl.com/api/ys.php"
        r = requests.get(url, allow_redirects=False)
        result = r.headers['Location']
        imgurl = 'https://api.starrobotwl.com/api/' + result
        return imgurl

    except Exception as e:
        embed = discord.Embed(title=f'{e}')
        return embed


class Genshinimg(InitCog):
    @app_commands.command(name='genshinimg')
    async def genshinimg(self, interaction: discord.Interaction):
        await interaction.response.defer()
        img = getimg()
        embed = discord.Embed()
        embed.set_image(url=img)
        await interaction.followup.send(embed=embed)


async def setup(client):
    await client.add_cog(Genshinimg(client))
