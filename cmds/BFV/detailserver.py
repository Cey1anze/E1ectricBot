import Paginator
import discord
import requests
from discord import app_commands

from Basic_bot.Core.init_cog import InitCog


def get_server(name):
    try:
        url = "https://api.gametools.network/bfv/detailedserver/?name={}&platform=pc&lang=zh-cn".format(name)
        r = requests.get(url)
        result = r.json()

        rotation = result['rotation']
        playerAmount = result['playerAmount']  # 玩家数
        maxPlayerAmount = result['maxPlayerAmount']  # 最大玩家数
        inQueue = result['inQueue']  # 等待队列
        prefix = result['prefix']  # 名称
        currentMap = result['currentMap']  # 当前地图
        currentMapImage = result['currentMapImage']  # img-url
        mode = result['mode']  # 模式

        gameId = result['gameId']
        detailurl = "https://gametools.network/servers/bfv/gameid/{}/pc".format(gameId)

        # 遍历rotation列表中的元素，并输出
        mapname_list = [item["mapname"] for item in rotation]
        image_list = [item["image"] for item in rotation]
        mode_list = [item["mode"] for item in rotation]

        page = {}
        for i in range(len(mapname_list)):
            page[i] = discord.Embed(title=f'接下来的轮换地图', colour=0x388ce5)
            page[i].add_field(name="地图名", value=f'{mapname_list[i]}', inline=True)
            page[i].add_field(name="模式", value=f'{mode_list[i]}', inline=True)
            page[i].add_field(name='\u200B', value='\u200B', inline=True)
            page[i].set_image(url=image_list[i])

        basic_embed = discord.Embed(title=f'{prefix}', url=detailurl, colour=0x388ce5)
        basic_embed.add_field(name='当前地图', value=f'{currentMap}', inline=True)
        basic_embed.add_field(name='模式', value=f'{mode}', inline=True)
        basic_embed.add_field(name='\u200B', value='\u200B', inline=True)

        basic_embed.add_field(name='当前玩家数', value=f'{playerAmount} / {maxPlayerAmount}', inline=True)
        basic_embed.add_field(name='等待队列', value=f'{inQueue}', inline=True)
        basic_embed.add_field(name='\u200B', value='\u200B', inline=True)
        basic_embed.set_image(url=currentMapImage)

        return page, basic_embed

    except Exception as e:
        print(e)
        embed = discord.Embed(title="出现错误", color=0x14aaeb)
        embed.add_field(name="Error", value="请求错误，暂时无法使用", inline=True)
        return embed


class Detailserver(InitCog):
    @app_commands.command(name='bfv-serverdetail', description='根据关键字查询某个服务器的具体信息')
    @app_commands.describe(name='关键字，不需要完整，但需要足够准确')
    async def detailserver(self, interaction: discord.Interaction, name: str):
        result = get_server(name)
        embed1 = result[1]
        embed2 = result[0]
        await interaction.response.defer()
        await interaction.channel.send(embed=embed1)
        await Paginator.Simple(timeout=999).start(interaction, pages=embed2)


async def setup(client):
    await client.add_cog(Detailserver(client))
