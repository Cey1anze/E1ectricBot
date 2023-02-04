import Paginator
import aiohttp
import discord
from discord import app_commands

from Core.init_cog import InitCog


async def get_bili_hot():
    page = {}
    coverlist = []
    titlelist = []
    hotlist = []
    imagelist = []
    updatelist = []
    urllist = []
    titlelist.clear()
    hotlist.clear()
    imagelist.clear()
    updatelist.clear()
    urllist.clear()
    try:
        async with aiohttp.ClientSession() as session:
            url = "https://api.gmit.vip/Api/BiliBliHot?format=json"
            async with session.get(url) as response:
                result = await response.json()
                for data in result['data']:
                    coverurl = "https://api.bilibili.com/x/web-interface/view?bvid={}".format((data['url'])[-12:])
                    async with session.get(coverurl) as response:
                        coverresult = await response.json()
                        cover = coverresult['data']['pic']
                        coverlist.append(
                            {'title': data['title'], 'url': data['url'], 'hot': data['hot'], 'cover': cover,
                             'updatetime': data['updatetime']})

        for item in coverlist:
            title = item['title']
            titlelist.append(title)
            hot = item['hot']
            hotlist.append(hot)
            img = item['cover']
            imagelist.append(img)
            update = item['updatetime']
            updatelist.append(update)
            url = item['url']
            urllist.append(url)

        for i in range(len(titlelist)):
            page[i] = discord.Embed(title=f'{titlelist[i]}', url='https:' + f'{urllist[i]}', colour=0x388ce5)
            page[i].add_field(name="观看次数", value=f'{hotlist[i]}', inline=True)
            page[i].add_field(name="数据更新时间", value=f'{updatelist[i]}', inline=True)
            page[i].add_field(name='\u200B', value='\u200B', inline=True)
            page[i].set_image(url=imagelist[i])

        return page

    except Exception as e:
        print(e)


class Bilileaderboard(InitCog):

    @app_commands.command(name='bilibili-leaderboard', description='展示当天的B站排行榜')
    async def bilileaderboard(self, interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            embed = await get_bili_hot()
            await Paginator.Simple(timeout=999).start(interaction, pages=embed)
        except Exception as e:
            await interaction.followup.send(e)


async def setup(client):
    await client.add_cog(Bilileaderboard(client))
