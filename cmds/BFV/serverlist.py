import Paginator
import discord
import requests
from discord import app_commands

from Basic_bot.Core.init_cog import InitCog


def get_serverlist():
    page = {}
    try:
        url = "https://api.gametools.network/bfv/servers/?name=%5BBFV%20ROBOT%5D&region=Asia&platform=pc&limit=100&lang=zh-cn"
        r = requests.get(url)
        result = r.json()

        # 提取servers列表中所有元素的prefix值
        prefix_list = [server['prefix'] for server in result['servers']]  # 服务器名称
        serverInfo_list = [server['serverInfo'] for server in result['servers']]  # 当前玩家数/总人数
        inQue_list = [server['inQue'] for server in result['servers']]  # 等待队列数
        url_list = [server['url'] for server in result['servers']]  # 当前地图图片url
        currentMap_list = [server['currentMap'] for server in result['servers']]  # 当前地图
        mode_list = [server['mode'] for server in result['servers']]  # 地图模式

        for i in range(len(prefix_list)):
            page[i] = discord.Embed(title=f'{prefix_list[i]}', description='默认只显示前100个', colour=0x388ce5)
            page[i].add_field(name="当前玩家数", value=f'{serverInfo_list[i]}', inline=True)
            page[i].add_field(name="等待队列", value=f'{inQue_list[i]}', inline=True)
            page[i].add_field(name='\u200B', value='\u200B', inline=True)

            page[i].add_field(name="当前地图", value=f'{currentMap_list[i]}', inline=True)
            page[i].add_field(name="模式", value=f'{mode_list[i]}', inline=True)
            page[i].add_field(name='\u200B', value='\u200B', inline=True)
            page[i].set_image(url=url_list[i])

        return page

    except Exception as e:
        print(e)
        embed = discord.Embed(title="出现错误", color=0x14aaeb)
        embed.add_field(name="Error", value="请求错误，暂时无法使用", inline=True)
        return embed


class Serverlist(InitCog):
    @app_commands.command(name='serverlist', description='查询当前机器人服列表')
    async def serverlist(self, interaction: discord.Interaction):
        try:
            embeds = get_serverlist()
            await Paginator.Simple(timeout=999).start(interaction, pages=embeds)
        except Exception as e:
            print(e)


async def setup(client):
    await client.add_cog(Serverlist(client))
