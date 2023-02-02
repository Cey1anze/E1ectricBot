"""
This module is meant to represent the Responses class
that will be used for MusicHelper
"""
import random
from time import gmtime, strftime
from typing import Literal, Optional

# Need to do this to separate the Response.discord attribute with the module itslf.
# Otherwise, the @staticmethod won't get type hints.
import discord as dpy
import lyricsgenius
import spotipy
import wavelink as wl
from spotipy import SpotifyException

from logs import settings
from cmds.Music.src.utils.functions import Functions

logger = settings.logging.getLogger(__name__)


class Responses(Functions):  # pylint:disable=too-many-public-methods
    """
    Holds methods for responding on interactions.
    """

    discord: dpy
    wavelink: wl
    spotify: spotipy.Spotify
    spot_exception: SpotifyException
    genius: lyricsgenius.Genius
    err_color: Literal
    sucess_color: Literal
    trending_uri: Optional[str]
    vote_url: Optional[str]
    invite_url: Optional[str]
    support_url: Optional[str]
    strftime: strftime
    gmtime: gmtime
    random: random
    url_regex: Literal

    async def user_not_in_vc(self):
        """
        When /join is used but member is not in a voice channel.
        """
        embed = self.discord.Embed(
            title="**你没有在语音频道中**", color=self.err_color
        )
        return embed

    async def in_vc(self):
        """
        When /join is used and member is in a voice channel.
        """
        embed = self.discord.Embed(
            title="**已加入语音频道**", color=self.sucess_color
        )
        return embed

    async def already_in_vc(self):
        """
        when /join is used while the Client is in a VoiceChannel
        """
        embed = self.discord.Embed(
            title="**已在语音频道中**", color=self.err_color
        )
        return embed

    async def left_vc(self):
        """
        When the Client leaves a channel
        """
        embed = self.discord.Embed(
            title="**离开了语音频道**", color=self.sucess_color
        )
        return embed

    async def already_left_vc(self):
        """
        when /leave is triggered and the client is not connected
        """
        embed = self.discord.Embed(
            title="**不在语音频道中**", color=self.err_color
        )
        return embed

    async def nothing_is_playing(self):
        """
        When nothing is playing
        """
        embed = self.discord.Embed(
            title="**现在没有播放的内容**.", color=self.err_color
        )
        return embed

    async def no_track_results(self):
        """
        When no tracks were found
        """
        embed = self.discord.Embed(
            title="**没有找到任何结果**", color=self.err_color
        )
        return embed

    async def display_track(
            self, track_info, guild_id, is_queued: bool, is_playing: bool
    ):
        """
        Displays the current track.
        """
        player = await self.get_player(guild_id)  ## Retrieve the player.

        if (
                not is_queued and player.loop
        ):  ## If the track is not queued and the loop is enabled.
            embed = self.discord.Embed(
                title="**正在播放 (歌曲循环已启用)**", color=self.sucess_color
            )

        elif (
                not is_queued and player.queue_loop
        ):  ## If the track is not queued and the queue loop is enabled.
            embed = self.discord.Embed(
                title="**正在播放 (队列循环已启用)**", color=self.sucess_color
            )

        elif (
                is_queued and player.loop
        ):  ## If both the track is queued and the loop is enabled.
            embed = self.discord.Embed(
                title="**Queued Track (Another Track Is Looping)**",
                color=self.sucess_color,
            )

        elif (
                is_queued and player.queue_loop
        ):  ## If both the track is queued and the queue loop is enabled.
            embed = self.discord.Embed(
                title="**Queued Track (Queue Loop Enabled)**", color=self.sucess_color
            )

        elif (
                is_queued and not player.loop
        ):  ## If the track is queued and the loop is not enabled.
            embed = self.discord.Embed(
                title="**Queued Track**", color=self.sucess_color
            )

        else:  ## If the track is not queued and the loop is not enabled.
            embed = self.discord.Embed(title="**正在播放**", color=self.sucess_color)

        try:  ## If the track_info already contains spotify info, don't make another request.
            title = track_info.title_url
            track_metadata = track_info
        except AttributeError:  ## Sometimes the track_info doesn't contain the spotify metadata.
            track_metadata = await self.gather_track_info(
                track_info.title, track_info.author, track_info
            )  ## Modify track info using spotify.

        embed.add_field(
            name="名称",
            value=f"[{track_metadata.title}]({track_metadata.title_url})",
            inline=False,
        )
        embed.add_field(
            name="作者",
            value=f"[{track_metadata.author}]({track_metadata.author_url})",
            inline=False,
        )
        embed.add_field(
            name="专辑",
            value=f"[{track_metadata.album}]({track_metadata.album_url})",
            inline=False,
        )

        if is_playing:  ## If /nowplaying is called, show the duration played.
            embed.add_field(
                name="进度条",
                value=f"{await self.format_duration(player.position)}/{await self.format_duration(track_metadata.duration)}",
                inline=False,
            )  ## Format the duration's into MM:SS

        else:  ## Otherwise, just show the track's duration.
            embed.add_field(
                name="时长",
                value=await self.format_duration(track_metadata.duration),
                inline=False,
            )

        embed.add_field(
            name="发布日期", value=track_metadata.release_date, inline=False
        )
        embed.set_thumbnail(url=track_metadata.cover_url)
        return embed

    async def started_playing(self):
        """
        When a Session has started
        """
        embed = self.discord.Embed(
            title="**Started Session.**", color=self.sucess_color
        )
        return embed

    async def show_queue(self, queue_info, guild_id):
        """
        Shows the queue
        """
        player = await self.get_player(guild_id)  ## Retrieve the player.
        queue_list = []  ## To store the tracks in the queue.
        title = "**Queue**"

        if len(queue_info) == 0:  ## If there are no tracks in the queue, respond.
            return await self.empty_queue()

        for i, track in enumerate(
                list(queue_info)[:20], start=1
        ):  ## Loop through all items in the queue.

            queue_list.append(
                f"**{i}.** [{track.title}]({track.title_url}) - [{track.author}]({track.author_url})"
            )  ## Add each track to the list.

        if player.queue_loop:  ## If the queue loop is enabled, change the title.
            title = "**Queue (Queue Loop Enabled)**"

        embed = self.discord.Embed(
            title=title,
            description="\n".join(queue_list),
            color=self.sucess_color,
        )

        embed.set_footer(text="Note: 最多显示20条歌曲")
        embed.set_thumbnail(url=queue_info[0].cover_url)
        return embed

    async def empty_queue(self):
        """
        Empties the queue
        """
        embed = self.discord.Embed(
            title="**播放队列为空**", color=self.err_color
        )
        return embed

    async def shuffled_queue(self):
        """
        When the queue has been shuffled
        """
        embed = self.discord.Embed(
            title="**已随机打乱播放队列**.", color=self.sucess_color
        )
        return embed

    async def volume_too_high(self):
        """
        When volume has reached 100% and Member tried to increase it.
        """
        embed = self.discord.Embed(
            title="**音量不能超过100%**", color=self.err_color
        )
        return embed

    async def volume_set(self, percentage: str):
        """
        Set the volume
        """
        embed = self.discord.Embed(
            title=f"**音量已被设置到 {percentage}%.**", color=self.sucess_color
        )
        return embed

    async def queue_track_actions(self, queue, track_index: int, embed_title: str):
        """
        Used for remove and skipto.
        """
        try:

            embed = self.discord.Embed(
                title=f"**{embed_title} {queue[track_index - 1].title} - {queue[track_index - 1].author}.**",
                color=self.sucess_color,
            )  ## The track exists in the queue.

        except IndexError:  ## If the track was not found in the queue, return False.
            return False

        return embed

    async def common_track_actions(self, track_info, embed_title: str):
        """
        Used for pause, resume, loop, queueloop.
        """
        if (
                track_info is None
        ):  ## If no track info is passed, just display the embed's title. Used in the case of queueloop.
            embed = self.discord.Embed(
                title=f"**{embed_title}.**", color=self.sucess_color
            )

        else:  ## Otherwise, display both.
            embed = self.discord.Embed(
                title=f"**{embed_title} {track_info.title} - {track_info.author}.**",
                color=self.sucess_color,
            )

        return embed

    async def track_not_in_queue(self):
        """
        When the track is not in a queue.
        """
        embed = self.discord.Embed(
            title="**Invalid track number.**", color=self.err_color
        )
        return embed

    async def no_tracks_in_queue(self):
        """
        No tracks in the queue.
        """
        embed = self.discord.Embed(
            title="**播放队列中已没有歌曲**",
            color=self.discord.Colour.dark_purple(),
        )
        return embed

    async def left_due_to_inactivity(self):
        """
        When the Client has been inactive
        and leaves.
        """
        embed = self.discord.Embed(
            title="**Left VC due to inactivity.**", color=self.err_color
        )
        return embed

    async def less_than_1_track(self):
        """
        When there is less than 1 track in queue.
        """
        embed = self.discord.Embed(
            title="**播放队列中至少需要1首歌曲**",
            color=self.err_color,
        )
        return embed

    async def added_playlist_to_queue(self):
        """
        When a playlist is added to the queue.
        """
        embed = self.discord.Embed(
            title="**已添加Spotify歌单到播放队列**", color=self.sucess_color
        )
        return embed

    async def cleared_queue(self):
        """
        When the queue has been cleared.
        """
        embed = self.discord.Embed(
            title="**已清空播放队列**", color=self.sucess_color
        )
        return embed

    async def invalid_url(self):
        """
        When the spotify url is invalid.
        """
        embed = self.discord.Embed(
            title="**不可用的Spotify URL**", color=self.err_color
        )
        return embed

    async def podcasts_not_supported(self):
        """
        When a spotify podcast or artist is provided instead of a track and playlist
        """
        embed = self.discord.Embed(
            title="**Spotify podcasts or artists are not supported.**",
            color=self.err_color,
        )
        return embed

    async def added_track(self, track_info):
        """
        When a track is added to the queue
        """
        embed = self.discord.Embed(
            title=f"**已添加 {track_info.title} - {track_info.author} 至播放队列**",
            color=self.sucess_color,
        )
        return embed

    async def only_spotify_urls(self):
        """
        When someone does not put a valid url
        """
        embed = self.discord.Embed(
            title="**只支持Spotify URL**", color=self.err_color
        )
        return embed

    async def display_new_releases(self, new_releases):
        """
        Shows the top 10 releases
        """
        embed = self.discord.Embed(title="**New Releases**", color=self.sucess_color)

        embed.add_field(
            name="Top 10",  ## Display all the newly released tracks,
            value="\n".join(
                [
                    f"**{i}.** [{item['name']}]({item['external_urls']['spotify']})"
                    for i, item in enumerate(new_releases["albums"]["items"], start=1)
                ]
            ),
        )

        embed.set_thumbnail(
            url=new_releases["albums"]["items"][0]["images"][0]["url"]
        )  ## Set the thumbnail to the newest track.
        return embed

    async def display_trending(self, trending):
        """
        Shows the top 10 trending songs
        """
        embed = self.discord.Embed(title="**Trending**", color=self.sucess_color)

        embed.add_field(
            name="Top 10",  ## Display all the trending tracks,
            value="\n".join(
                [
                    f"**{i}.** [{item['track']['name']}]({item['track']['external_urls']['spotify']}) - {item['track']['artists'][0]['name']}"
                    for i, item in enumerate(trending["items"], start=1)
                ]
            ),
        )

        embed.set_thumbnail(
            url=trending["items"][0]["track"]["album"]["images"][0]["url"]
        )  ## Set the thumbnail to the top trending track.
        return embed

    async def display_playlist(self, playlist_url):
        """
        shows all the tracks from a playlist url
        """
        playlist_info = await self.playlist_info(
            playlist_url
        )  ## Retrieve info about the playlist.

        embed = self.discord.Embed(title="**Queued Playlist**", color=self.sucess_color)
        embed.add_field(
            name="Name",
            value=f"[{playlist_info['name']}]({playlist_info['external_urls']['spotify']})",
            inline=False,
        )

        embed.add_field(
            name="User",
            value=f"[{playlist_info['owner']['display_name']}]({playlist_info['owner']['external_urls']['spotify']})",
            inline=False,
        )

        embed.add_field(
            name="Tracks", value=playlist_info["tracks"]["total"], inline=False
        )
        embed.set_thumbnail(
            url=playlist_info["images"][0]["url"]
        )  ## Set the thumbnail to the playlist's artwork.
        return embed

    async def display_album(self, album_url):
        """
        Displays the album
        """
        album_info = await self.album_info(
            album_url
        )  ## Retrieve info about the playlist.

        embed = self.discord.Embed(title="**Queued Album**", color=self.sucess_color)
        embed.add_field(
            name="Name",
            value=f"[{album_info['name']}]({album_info['external_urls']['spotify']})",
            inline=False,
        )

        embed.add_field(
            name="Artist",
            value=f"[{album_info['artists'][0]['name']}]({album_info['artists'][0]['external_urls']['spotify']})",
            inline=False,
        )

        embed.add_field(
            name="Release Date", value=album_info["release_date"], inline=False
        )
        embed.add_field(name="Tracks", value=album_info["total_tracks"], inline=False)
        embed.set_thumbnail(
            url=album_info["images"][0]["url"]
        )  ## Set the thumbnail to the album's artwork
        return embed

    async def display_vote(self):
        """
        Used for the vote command.
        """
        view = self.discord.ui.View()
        style = self.discord.ButtonStyle.gray
        item = self.discord.ui.Button(style=style, label="Vote!", url=self.vote_url)
        view.add_item(item=item)

        embed = self.discord.Embed(
            title="**Click the button below to vote for me!**", color=self.sucess_color
        )
        return embed, view

    async def display_invite(self):
        """
        Used for the invite command.
        """
        view = self.discord.ui.View()
        style = self.discord.ButtonStyle.gray
        item = self.discord.ui.Button(style=style, label="Invite!", url=self.invite_url)
        view.add_item(item=item)

        embed = self.discord.Embed(
            title="**Click the button below to invite me!**", color=self.sucess_color
        )
        return embed, view

    async def display_support(self):
        """
        Used for the support command.
        """
        view = self.discord.ui.View()
        style = self.discord.ButtonStyle.gray
        item = self.discord.ui.Button(
            style=style, label="Support!", url=self.support_url
        )
        view.add_item(item=item)

        embed = self.discord.Embed(
            title="**Click the button below join my support server!**",
            color=self.sucess_color,
        )
        return embed, view

    async def display_lyrics(self, lyrics):
        """
        Displays the lyrics.
        """
        embed = self.discord.Embed(
            title="Lyrics", description=lyrics, color=self.sucess_color
        )
        return embed

    async def lyrics_too_long(
            self,
    ):
        """
        When the lyrics are over 4096 characters long.
        """
        embed = self.discord.Embed(
            title="**The Lyrics in this song are over 4096 characters!**",
            color=self.err_color,
        )
        return embed

    async def log_track_started(self, track, guild_id):
        """
        Sends to the dedicated LOG channel.
        >> A track has been added.
        """
        embed = self.discord.Embed(
            title=f"**{track.title} - {track.author} 已在: {guild_id} 上开始播放**",
            color=self.sucess_color,
        )
        return embed

    async def log_track_finished(self, track, guild_id):
        """
        sends a dedicated LOG message.
        >> A track has finished.
        """
        embed = self.discord.Embed(
            title=f"**{track.title} - {track.author} 已在: {guild_id} 上完成播放**",
            color=self.err_color,
        )
        return embed

    async def display_search(self, search_query):
        """
        Displays the search results.
        """
        search_results = await self.search_songs(
            search_query
        )  ## Retrieve search results.
        formatted_results = await self.format_search_results(
            search_results
        )  ## Format the search results.

        embed = self.discord.Embed(
            title="**Search Results**",
            description=formatted_results,
            color=self.sucess_color,
        )

        embed.set_thumbnail(
            url=search_results["tracks"]["items"][0]["album"]["images"][0]["url"]
        )  ## Set the thumbnail to the first track's artwork.
        embed.set_footer(
            text="Tip: Copy any one of the track or album hyperlinks and play them with /url."
        )
        return embed

    async def already_paused(self, track_info):
        """
        When the wavelink player is already paused.
        """
        embed = self.discord.Embed(
            title=f"**{track_info.title} - {track_info.author} 已经被暂停!**",
            color=self.err_color,
        )
        return embed

    async def already_resumed(self, track_info):
        """
        When the wavelink player is already resumed.
        """
        embed = self.discord.Embed(
            title=f"**{track_info.title} - {track_info.author} 已经被继续播放!**",
            color=self.err_color,
        )
        return embed

    @staticmethod
    async def on_joining_guild(guild: dpy.Guild):
        """
        Embed for when braum joins a server.
        """
        embed = dpy.Embed(
            title=f"**BRAUM HAS JOINED** -->, {guild.name}\nOwner is ``@{guild.owner.name}#{guild.owner.discriminator}``\nThis server has {guild.member_count} members!",
            color=dpy.Colour.green(),
        )
        return embed

    @staticmethod
    async def on_leaving_guild(guild: dpy.Guild):
        """
        Embed for when braum leaves a server.
        """
        embed = dpy.Embed(
            title=f"**BRAUM HAS LEFT** -->, {guild.name}\nOwner was ``@{guild.owner.name}#{guild.owner.discriminator}``\nThis server had {guild.member_count} members!",
            color=dpy.Colour.green(),
        )
        return embed

    async def already_in_voicechannel(self, channel: wl.player.VoiceChannel):
        """
        When the client is already connected to a voice channel.
        """
        embed = self.discord.Embed(
            title="**Dj braum is already connected to a voice channel!**",
            description=f"Join me here --> <#{channel.id}>",
            color=self.err_color,
        )
        return embed
