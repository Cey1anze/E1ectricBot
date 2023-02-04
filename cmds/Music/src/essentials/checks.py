"""
This module holds all appcommand.checks. 
They will raise an error if condition is not met.

They will be used as decorators for common commands.
"""
import discord
import wavelink
from discord import app_commands
from discord.ext import commands
from logs import settings

from .errors import MustBeSameChannel, NotConnectedToVoice, PlayerNotConnected, MustBeInNsfwChannel

logger = settings.logging.getLogger(__name__)


def member_in_voicechannel():
    """If member is connected to a voice chat"""

    async def predicate(interaction: discord.Interaction) -> bool:
        if not interaction.user.voice:  ## If user is not in a VC, respond.
            raise NotConnectedToVoice("你没有连接到语音频道!")
        return True

    return app_commands.check(predicate)


def player_connected():
    async def predicate(interaction: discord.Interaction):
        player: wavelink.Player = wavelink.NodePool.get_node().get_player(
            guild=interaction.guild
        )

        if not player.is_connected:
            raise PlayerNotConnected("机器人未连接到任何语音频道!")
        return True

    return app_commands.check(predicate)


def in_same_channel():
    async def predicate(interaction: discord.Interaction):
        player: wavelink.Player = wavelink.NodePool.get_node().get_player(
            guild=interaction.guild
        )
        try:
            if player.channel.id != interaction.user.voice.channel.id:
                raise MustBeSameChannel(
                    "请加入机器人连接的频道"
                )
        except AttributeError:
            pass
        return True

    return app_commands.check(predicate)


def in_nsfw_channel():
    def predicate(ctx):
        if not ctx.guild:
            return
        if ctx.channel.is_nsfw():
            return True
        else:
            raise MustBeInNsfwChannel()

    return commands.check(predicate)


def allowed_to_connect():
    """Checks if the Client has permissions to join the current members voice channel"""

    def predicate(interaction: discord.Interaction):
        if (
                interaction.user.voice.channel.permissions_for(interaction.guild.me)
                == discord.Permissions.connect
        ):
            return True

    return app_commands.check(predicate)
