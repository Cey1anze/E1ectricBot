import asyncio
import base64
import binascii
import json
import random
import string
from urllib import parse
from Crypto.Cipher import AES

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
        if Helper.not_connceted_client(self.voice_client):
            await interaction.followup.send(embed=Response.bot_not_joined())
        else:
            await interaction.response.defer()
            # 使机器人强制离开
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
        """

        根据歌名搜索歌曲
        btw，本来不想做这个功能的，直接输入网易云链接用/netease-play不香吗，这个功能又麻烦还累，但是还是做出来了，这还不来个Star？
        为什么不用request呢，如果你看到了这个注释，请看下面的各种方法，你就知道我为什么要花大力气去这样搞而不是选择用request了

        :param interaction: discord.Interaction
        :param song_name: 歌名

        """

        global song_url
        song_urllist = []
        song_urllist.clear()

        def get_random():
            random_str = ''.join(random.sample(string.ascii_letters + string.digits, 16))
            return random_str

        # AES加密要求加密的文本长度必须是16的倍数，密钥的长度固定只能为16,24或32位，因此我们采取统一转换为16位的方法
        def len_change(text):
            pad = 16 - len(text) % 16
            text = text + pad * chr(pad)
            text = text.encode("utf-8")
            return text

        # AES加密方法
        def aes(text, key):
            # 首先对加密的内容进行位数补全，然后使用 CBC 模式进行加密
            iv = b'0102030405060708'
            text = len_change(text)
            cipher = AES.new(key.encode(), AES.MODE_CBC, iv)
            encrypted = cipher.encrypt(text)
            encrypt = base64.b64encode(encrypted).decode()
            return encrypt

        # js中的 b 函数，调用两次 AES 加密
        # text 为需要加密的文本， str 为生成的16位随机数
        def b(text, str):
            first_data = aes(text, '0CoJUm6Qyw8W8jud')
            second_data = aes(first_data, str)
            return second_data

        # 这就是那个巨坑的 c 函数
        def c(text):
            e = '010001'
            f = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
            text = text[::-1]
            result = pow(int(binascii.hexlify(text.encode()), 16), int(e, 16), int(f, 16))
            return format(result, 'x').zfill(131)

        # 获取最终的参数 params 和 encSecKey 的方法
        def get_final_param(text, str):
            params = b(text, str)
            encSecKey = c(str)
            return {'params': params, 'encSecKey': encSecKey}

        # 通过参数获取搜索歌曲的列表
        def get_music_list(params, encSecKey):
            url = "https://music.163.com/weapi/cloudsearch/get/web?csrf_token="

            payload = 'params=' + parse.quote(params) + '&encSecKey=' + parse.quote(encSecKey)
            headers = {
                'authority': 'music.163.com',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
                'content-type': 'application/x-www-form-urlencoded',
                'accept': '*/*',
                'origin': 'https://music.163.com',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://music.163.com/search/',
                'accept-language': 'zh-CN,zh;q=0.9',
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            return response.text

        # 通过歌曲的id获取播放链接
        def get_reply(params, encSecKey):
            url = "https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token="
            payload = 'params=' + parse.quote(params) + '&encSecKey=' + parse.quote(encSecKey)
            headers = {
                'authority': 'music.163.com',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
                'content-type': 'application/x-www-form-urlencoded',
                'accept': '*/*',
                'origin': 'https://music.163.com',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://music.163.com/',
                'accept-language': 'zh-CN,zh;q=0.9'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            return response.text

        def check(num):
            return num.author == interaction.user and num.content.isdigit() and int(num.content) in range(0,
                                                                                                          len(song_list))

        def is_bot_message(message):
            return message.author.bot

        d = {"hlpretag": "<span class=\"s-fc7\">", "hlposttag": "</span>", "s": song_name, "type": "1", "offset": "0",
             "total": "true", "limit": "30", "csrf_token": ""}
        d = json.dumps(d)
        random_param = get_random()
        param = get_final_param(d, random_param)
        song_list = get_music_list(param['params'], param['encSecKey'])
        if len(song_list) > 0:
            song_list = json.loads(song_list)['result']['songs']
            for i, item in enumerate(song_list):
                item = json.dumps(item)
                d = {"ids": "[" + str(json.loads(str(item))['id']) + "]", "level": "standard", "encodeType": "",
                     "csrf_token": ""}
                d = json.dumps(d)
                param = get_final_param(d, random_param)
                song_info = get_reply(param['params'], param['encSecKey'])
                if len(song_info) > 0:
                    song_info = json.loads(song_info)
                    song_url = json.dumps(song_info['data'][0]['url'], ensure_ascii=False)
                    song_urllist.append(song_url.replace('"', ''))
                    if song_urllist[i] == 'null':
                        status = "无法获取歌曲资源"
                    else:
                        status = "获取歌曲资源成功"
                    content = str(i) + "：" + json.loads(str(item))['name'] + " - " + json.loads(str(item))['ar'][0][
                        'name'] + " - " + status
                    await interaction.channel.send(content)
                else:
                    await interaction.followup.send("该首歌曲解析失败，可能是因为歌曲格式问题")

            await interaction.channel.send('请输入序号(超时时间：60s)')
            selection = await self.client.wait_for('message', check=check, timeout=60.0)
            selceted_url = song_urllist[int(selection.content)]
            self.voice_client = await interaction.user.voice.channel.connect()
            self.voice_client.play(discord.FFmpegPCMAudio(selceted_url))
            self.voice_client.source = discord.PCMVolumeTransformer(self.voice_client.source)
            self.voice_client.source.volume = current_volume

            await asyncio.sleep(10)
            await interaction.channel.purge(limit=len(song_list) + 1, check=is_bot_message)
        else:
            await interaction.followup.send("很抱歉，未能搜索到相关歌曲信息")

        # 输入序号直接开始播放

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
