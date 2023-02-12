import discord
from discord import app_commands
from Core.init_cog import InitCog


class Netease(InitCog):
    current_volume = 0.7

    @app_commands.command(name='netease-join', description='让机器人进入语音频道')
    async def join(self, interaction: discord.Interaction):
        """
        让机器人进入语音频道
        """
        await interaction.response.defer()
        if not interaction.user.voice:
            embed = discord.Embed(title='请先加入语音频道', color=discord.Color.red())
            await interaction.followup.send(embed=embed)
            return
        await interaction.user.voice.channel.connect(self_deaf=True)
        await interaction.followup.send(embed=discord.Embed(title='已加入语音频道', colour=discord.Color.green()))

    @app_commands.command(name='netease-leave', description='让机器人离开语音频道')
    async def leave(self, interaction: discord.Interaction):
        """
        让机器人离开语音频道
        """
        await interaction.response.defer()
        await interaction.guild.voice_client.disconnect(force=True)
        await interaction.followup.send(embed=discord.Embed(title='已离开语音频道', colour=discord.Color.green()))

    @app_commands.command(name='netease-vol', description='设置播放音量')
    @app_commands.describe(volume='设置音量（输入 0 ~ 1 之间的数字）')
    async def set_vol(self, interaction: discord.Interaction, volume: float):
        """
        设置音量
        :param volume: 音量值(0~1)
        """
        global current_volume
        await interaction.response.defer()
        if not self.voice_client:
            embed = discord.Embed(title='请先播放音乐', color=discord.Color.red())
            await interaction.followup.send(embed=embed)
            return

        if volume < 0 or volume > 1:
            embed = discord.Embed(title='请输入0~1的数字', color=discord.Color.red())
            await interaction.followup.send(embed=embed)
            return

        self.voice_client.source.volume = volume
        await interaction.followup.send(
            embed=discord.Embed(title='已设置音量为{}%'.format(volume * 100), color=discord.Color.green()))

    @app_commands.command(name='netease-play', description='播放网易云音乐')
    async def play(self, interaction: discord.Interaction, url: str):
        """
        播放网易云音乐
        :param url: 网易云mp3直链
        """
        await interaction.response.defer()
        if not interaction.user.voice:
            embed = discord.Embed(title='请先加入语音频道', color=discord.Color.red())
            await interaction.followup.send(embed=embed)
            return
        self.voice_client = await interaction.user.voice.channel.connect()
        self.voice_client.play(discord.FFmpegPCMAudio(url))
        self.voice_client.source = discord.PCMVolumeTransformer(self.voice_client.source)
        self.voice_client.source.volume = current_volume


async def setup(client):
    await client.add_cog(Netease(client))
