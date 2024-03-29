import discord
from discord import app_commands
from Core.init_cog import InitCog
from cmds.Netease_Dev import Functions
import cmds.Netease_Dev.Response as Response
import cmds.Netease_Dev.Music_Helper as Helper

current_volume = 70


class Netease(InitCog):
    def __init__(self, client):
        super().__init__(client)
        self.voice_client = None
        self.current_song_url = None

    @app_commands.command(name='netease-join', description='让机器人进入语音频道')
    async def join(self, interaction: discord.Interaction):
        """
        让机器人进入语音频道
        """
        await interaction.response.defer()
        if Helper.user_not_connected(interaction):
            await interaction.followup.send(embed=Response.user_not_joined())
            return
        await interaction.user.voice.channel.connect(self_deaf=True)
        await interaction.followup.send(embed=Response.joined_voice())

    @app_commands.command(name='netease-leave', description='让机器人离开语音频道')
    async def leave(self, interaction: discord.Interaction):
        """
        让机器人离开语音频道
        """
        if Helper.not_connceted_client(self.voice_client):
            await interaction.followup.send(embed=Response.bot_not_joined())
        else:
            await interaction.response.defer()
            # 使机器人强制离开
            await interaction.guild.voice_client.disconnect(force=True)
            await interaction.followup.send(embed=Response.leaved_voice())

    @app_commands.command(name='netease-vol', description='设置播放音量')
    @app_commands.describe(volume='设置音量（输入 0 ~ 100 之间的数字）')
    async def set_vol(self, interaction: discord.Interaction, volume: int):
        """
        设置音量
        """
        await interaction.response.defer()
        if Helper.not_connceted_client(self.voice_client):
            await interaction.followup.send(embed=Response.music_not_playing())
            return

        if volume < 0 or volume > 100:
            await interaction.followup.send(embed=Response.vol_input_error())
            return

        self.voice_client.source.volume = volume / 100
        await interaction.followup.send(embed=Response.vol_setted(volume / 100))

    @app_commands.command(name='netease-search')
    async def search(self, interaction: discord.Interaction, *, name_or_id: str):
        """
        根据歌名搜索歌曲

        :param interaction: discord.Interaction
        :param name_or_id: 歌名
        """
        """
        btw，本来不想做这个功能的，直接输入网易云链接用 / netease - play不香吗，这个功能又麻烦还累，但是还是做出来了，这还不来个Star？
        为什么不用request呢，如果你看到了这个注释，请看下面调用的各种方法，你就知道我为什么要花大力气去这样搞而不是选择用request了
        """
        global current_volume
        song_urllist = []
        await interaction.response.defer()
        if Helper.user_not_connected(interaction):
            await interaction.followup.send(embed=Response.user_not_joined())
            return
        data = Functions.get_song_url(name_or_id)
        if isinstance(data, tuple):
            song_embed = data[0]
            song_list = data[1]
            song_urllist = data[2]
            await interaction.channel.send(embed=song_embed, delete_after=60.0)
            # 输入序号直接开始播放
            await interaction.channel.send(content=f'{interaction.user.mention}请输入序号', delete_after=60.0)

            def check(num):
                return num.author == interaction.user and num.content.isdigit() and int(num.content) in range(0,
                                                                                                              len(song_list))

            selection = await self.client.wait_for('message', check=check)
            selected_url = song_urllist[int(selection.content)]
            self.current_song_url = selected_url

            if not interaction.guild.voice_client:
                self.voice_client = await interaction.user.voice.channel.connect()

            await self.voice_client.move_to(interaction.user.voice.channel)
            self.voice_client.play(discord.FFmpegPCMAudio(selected_url))
            self.voice_client.source = discord.PCMVolumeTransformer(self.voice_client.source)
            self.voice_client.source.volume = current_volume
            await interaction.followup.send(f"即将播放：{song_list[int(selection.content)]['name']}")

            song_name = song_list[int(selection.content)]['name']
            author = song_list[int(selection.content)]['ar'][0]['name']
            album_name = song_list[int(selection.content)]['al']['name']
            publish_time = Functions.time_switch(song_list[int(selection.content)]['publishTime'])
            album_pic_url = song_list[int(selection.content)]['al']['picUrl']

            await interaction.channel.send(
                embed=Response.track_info(song_name, author, album_name, publish_time, album_pic_url))
        else:
            await interaction.followup.send(embed=data)

    @app_commands.command(name='netease-play', description='播放网易云音乐')
    async def play(self, interaction: discord.Interaction, url: str):
        """
        播放网易云音乐

        :param interaction: discord.Interaction
        :param url: 网易云mp3直链
        """
        await interaction.response.defer()
        if Helper.user_not_connected(interaction):
            await interaction.followup.send(embed=Response.user_not_joined())
            return
        self.voice_client = await interaction.user.voice.channel.connect()
        self.voice_client.play(discord.FFmpegPCMAudio(url))
        self.voice_client.source = discord.PCMVolumeTransformer(self.voice_client.source)
        self.voice_client.source.volume = current_volume

    @app_commands.command(name='netease-pause', description='暂停播放')
    async def pause(self, interaction: discord.Interaction):
        """
        暂停播放
        """
        await interaction.response.defer()
        if self.voice_client.is_playing() is False:
            await interaction.followup.send(embed=Response.music_not_playing())
            return
        self.voice_client.pause()
        await interaction.followup.send(embed=Response.music_paused())

    @app_commands.command(name='netease-resume', description='继续播放')
    async def resume(self, interaction: discord.Interaction):
        """
        继续播放
        """
        await interaction.response.defer()
        if self.voice_client.is_paused() is False:
            await interaction.followup.send(embed=Response.music_not_paused())
            return
        self.voice_client.resume()
        await interaction.followup.send(embed=Response.music_resumed())

    @app_commands.command(name='netease-stop', description='停止播放')
    async def stop(self, interaction: discord.Interaction):
        """
        停止播放
        """
        await interaction.response.defer()
        if self.voice_client.is_playing() is False:
            await interaction.followup.send(embed=Response.music_not_playing())
            return
        self.current_song_url = None
        self.voice_client.stop()
        await interaction.followup.send(embed=Response.music_stoped())


async def setup(client):
    await client.add_cog(Netease(client))
