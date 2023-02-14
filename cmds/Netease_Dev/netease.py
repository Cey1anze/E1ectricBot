import asyncio
import re
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options

import discord
import requests
from discord import app_commands
from Core.init_cog import InitCog
import cmds.Netease_Dev.Embed_Response as Response
import cmds.Netease_Dev.Music_Helper as Helper


class Netease(InitCog):
    current_volume = 0.7

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
        await interaction.response.defer()
        await interaction.guild.voice_client.disconnect(force=True)
        await interaction.followup.send(embed=Response.leaved_voice())

    @app_commands.command(name='netease-vol', description='设置播放音量')
    @app_commands.describe(volume='设置音量（输入 0 ~ 1 之间的数字）')
    async def set_vol(self, interaction: discord.Interaction, volume: float):
        """
        设置音量
        param volume: 音量值(0~1)
        """
        global current_volume
        await interaction.response.defer()
        if Helper.not_connceted_client(self.voice_client):
            await interaction.followup.send(embed=Response.music_not_playing())
            return

        if volume < 0 or volume > 1:
            await interaction.followup.send(embed=Response.vol_input_error())
            return

        self.voice_client.source.volume = volume
        await interaction.followup.send(embed=Response.vol_setted(volume))

    @app_commands.command(name='netease-search')
    async def search(self, interaction: discord.Interaction, *, song_name: str):
        await interaction.response.defer()
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')

        global response, content
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
        }

        # 指定url

        url_1 = 'https://music.163.com/#/search/m/?s=' + song_name + '&type=1'

        # 初始化browser对象
        browser = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=chrome_options)

        # 访问该url
        browser.get(url=url_1)

        # 由于网页中有iframe框架，进行切换
        browser.switch_to.frame('g_iframe')

        # 等待0.5秒
        sleep(0.5)

        # 抓取到页面信息
        page_text = browser.execute_script("return document.documentElement.outerHTML")

        # 退出浏览器
        browser.quit()

        ex1 = '<a.*?id="([0-9]*?)"'
        ex2 = '<b.*?title="(.*?)"><span class="s-fc7">'
        ex3 = 'class="td w1"><div.*?class="text"><a.*?href=".*?">(.*?)</a></div></div>'

        id_list = re.findall(ex1, page_text, re.M)[::2][:5]

        song_list = re.findall(ex2, page_text, re.M)[:5]

        singer_list = re.findall(ex3, page_text, re.M)[:5]

        available_list = []
        available_list.clear()

        for i in range(len(singer_list)):
            singer_list[i] = re.sub('</a>/<a href="/artist\?id=.*?">', ',', singer_list[i])

        for song_id in id_list:
            url = "http://music.163.com/song/media/outer/url?id=" + str(song_id) + ".mp3"
            response = requests.get(url, headers=headers, allow_redirects=False)
            sleep(1)
            if response.headers['Location'] == "http://music.163.com/404":
                available_list.append("资源异常")
            else:
                available_list.append("资源正常")

        for i in range(len(id_list)):
            content = str(i + 1) + '.' + str(song_list[i]) + '\t-' + '\t' + str(singer_list[i]) + '\t-' + '\t' + str(
                available_list[i]) + '\n'

            await interaction.channel.send(content)

        def check(num):
            return num.author == interaction.user and num.content.isdigit() and int(num.content) in range(1, 6)

        try:
            await interaction.followup.send('请输入序号(超时时间：60s)')
            selection = await self.client.wait_for('message', check=check, timeout=60.0)
        except asyncio.TimeoutError:
            await interaction.followup.send("选择超时")
        else:
            selceted_id = id_list[int(selection.content) - 1]

            selceted_url = "http://music.163.com/song/media/outer/url?id=" + str(selceted_id) + ".mp3"

            self.voice_client = await interaction.user.voice.channel.connect()
            self.voice_client.play(discord.FFmpegPCMAudio(selceted_url))
            self.voice_client.source = discord.PCMVolumeTransformer(self.voice_client.source)
            self.voice_client.source.volume = current_volume

    @app_commands.command(name='netease-play', description='播放网易云音乐')
    async def play(self, interaction: discord.Interaction, url: str):
        """
        播放网易云音乐
        param url: 网易云mp3直链
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
        self.voice_client.stop()
        await interaction.followup.send(embed=Response.music_stoped())


async def setup(client):
    await client.add_cog(Netease(client))
