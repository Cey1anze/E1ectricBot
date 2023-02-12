import discord
import requests
from discord import app_commands
from Core.init_cog import InitCog


def get60s():
    try:
        url = "http://www.lpv4.cn:10000/api/60s"
        r = requests.get(url, allow_redirects=False)
        result = r.headers['Location']
        return result

    except Exception as e:
        print(e)


class Sixty(InitCog):

    @app_commands.command(name='60s', description='每天60s读懂世界')
    async def sixty(self, interaction: discord.Interaction):
        await interaction.response.defer()
        img = get60s()
        embed = discord.Embed()
        embed.set_image(url=img)
        await interaction.followup.send(embed=embed)


async def setup(client):
    await client.add_cog(Sixty(client))
