"""General discord Cog"""

import discord
from discord import app_commands
from discord.ext import commands

from logs import settings
from cmds.Music.src.utils.music_helper import MusicHelper

logger = settings.logging.getLogger(__name__)


class General(commands.Cog):
    """
    Cog for General commands.
    """

    bot: commands.Bot

    def __init__(self, bot) -> None:
        self.bot = bot
        self.music = MusicHelper()

    @app_commands.command(
        name="music-newreleases",
        description="展示最新发布的歌曲",
    )
    async def newreleases(self, interaction: discord.Interaction):
        """
        Shows the 10 latest releases
        """
        await interaction.response.defer()

        return await interaction.followup.send(
            embed=await self.music.display_new_releases(
                await self.music.get_new_releases()
            )
        )  ## Display the trending embed.

    @app_commands.command(
        name="music-trending", description="展示当天的流行趋势"
    )
    async def trending(self, interaction: discord.Interaction):
        """
        Shows the trending chart
        """
        await interaction.response.defer()

        return await interaction.followup.send(
            embed=await self.music.display_trending(await self.music.get_trending())
        )  ## Display the new releases embed.

    @app_commands.command(
        name="music-search", description="搜索Spotify的曲目"
    )
    @app_commands.describe(search_query="要搜索的歌曲名称")
    async def search(self, interaction: discord.Interaction, *, search_query: str):
        """
        Search command for
        """
        await interaction.response.defer()

        return await interaction.followup.send(
            embed=await self.music.display_search(search_query)
        )  ## Display the invite embed.

    @app_commands.command(
        name="music-lyrics", description="找到 (几乎) 任何歌曲的歌词"
    )
    @app_commands.describe(song_name="检索歌词的歌曲名称")
    async def lyrics(self, interaction: discord.Interaction, *, song_name: str):
        """
        /lyrics command
        """
        await interaction.response.defer(
            ephemeral=True
        )  ## Send as an ephemeral to avoid clutter.

        lyrics_embed = await self.music.display_lyrics(
            await self.music.get_lyrics(song_name)
        )  ## Retrieve the lyrics and embed it.

        try:
            return await interaction.followup.send(
                embed=lyrics_embed
            )  ## Display the lyrics embed.
        except discord.HTTPException:  ## If the lyrics are more than 4096 characters, respond.
            return await interaction.followup.send(
                embed=await self.music.lyrics_too_long()
            )


async def setup(bot):
    """
    Setup the cog.
    """
    await bot.add_cog(General(bot))
