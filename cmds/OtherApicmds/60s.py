import discord
from discord import app_commands
from Core.init_cog import InitCog


class Sixty(InitCog):

    @app_commands.command(name='60s', description='每天60s读懂世界')
    async def sixty(self, interaction: discord.Interaction):
        await interaction.response.defer()
        embed = discord.Embed()
        embed.set_image(url="https://zj.v.api.aa1.cn/api/60s-v2/?cc=e1e'bot'")
        await interaction.followup.send(embed=embed)


async def setup(client):
    await client.add_cog(Sixty(client))
