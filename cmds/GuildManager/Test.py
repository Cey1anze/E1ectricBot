import discord
from discord import app_commands
from Core.init_cog import InitCog


class Test(InitCog):

    @app_commands.command(name='ping', description='测试机器人的延迟')
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await interaction.followup.send(embed=discord.Embed(description=f'🕒延迟：{round(self.client.latency * 1000)} ms',
                                                            colour=discord.Color.from_rgb(130, 156, 242)))


async def setup(client):
    await client.add_cog(Test(client))
