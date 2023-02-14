import discord
from Core.init_cog import InitCog


def user_not_connected(interaction: discord.Interaction) -> bool:
    return interaction.user.voice is None


def not_connceted_client(voice_client: discord.VoiceClient) -> bool:
    return voice_client is None


class Helper(InitCog):
    pass


async def setup(client):
    await client.add_cog(Helper(client))
