import discord
from discord import app_commands
from Core.init_cog import InitCog


class Netease(InitCog):

    @app_commands.command(name='netease')
    async def play(self, interaction: discord.Interaction, url: str):
        await interaction.response.defer()
        voice = await interaction.user.voice.channel.connect()
        voice.play(discord.FFmpegPCMAudio(url))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.7


async def setup(client):
    await client.add_cog(Netease(client))
