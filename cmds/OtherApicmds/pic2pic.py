import discord
import requests
import Paginator

from discord import app_commands, Embed
from Core.init_cog import InitCog

similarity: str
similaritylist = []
similaritylist.clear()
creator: str
creatorlist = []
creatorlist.clear()
ext_urls: str
ext_urlslist = []
ext_urlslist.clear()
source: str
sourcelist = []
sourcelist.clear()
material: str
materiallist = []
materiallist.clear()


def get_picinfo(pic) -> dict[int, Embed]:
    global similarity, creator, ext_urls, source, material
    num = -1
    pic2pic = {}
    clienterror = {}
    servererror = {}
    url = "https://saucenao.com/search.php?api_key=a82a24ef646627d7a944aaccff50db680c5c9b3a&db=999&output_type=2&&numres=5&url={}".format(
        pic)
    r = requests.get(url)
    result = r.json()

    if result['header']['index']['0']['status'] < 0:  # 客户端异常
        clienterror[0] = discord.Embed(title='请求错误', description='客户端异常,包括但不限于图像损坏, 不在搜索范围内等', colour=0xf44336)
        return clienterror
    if result['header']['index']['0']['status'] > 0:
        servererror[0] = discord.Embed(title='请求错误', description='服务端异常,包括但不限于生成结果失败, 搜索失败等', colour=0xf44336)
        return servererror
    else:
        for i in range(len(result['results'])):
            if 'creator' in result['results'][i]['data'] and 'source' in result['results'][i]['data'] and 'ext_urls' in \
                    result['results'][i]['data'] and 'material' in result['results'][i]['data']:
                num = num + 1
                similarity = result['results'][i]['header']['similarity']  # 相似度
                similaritylist.append(similarity)
                ext_urls = result['results'][i]['data']['ext_urls'][0]  # 额外链接
                ext_urlslist.append(ext_urls)
                creator = result['results'][i]['data']['creator']  # 作者
                creatorlist.append(creator)
                source = result['results'][i]['header']['thumbnail']  # 来源链接
                sourcelist.append(source)
                material = result['results'][i]['data']['material']  # 类别
                materiallist.append(material)

                pic2pic[num] = discord.Embed(title='搜图结果', colour=0x388ce5)
                pic2pic[num].add_field(name='图片相似度', value=f'{similaritylist[num]} %', inline=False)
                pic2pic[num].add_field(name='作者', value=f'{creatorlist[num]}', inline=False)
                pic2pic[num].add_field(name='类别', value=f'{materiallist[num]}', inline=False)
                pic2pic[num].add_field(name='原贴链接 (Sir,This way~~)', value=f'{ext_urlslist[num]}', inline=False)
                pic2pic[num].set_image(url=sourcelist[num])
                pic2pic[num].set_footer(text='Powered by SauceNAO')

        return pic2pic


class Pic2Pic(InitCog):
    @app_commands.command(name='pic2pic', description='以图搜图（动画、漫画、插画作品、二次元图片）')
    @app_commands.describe(pic='需要查找的图片，必须是链接（可以将图片私信给机器人，再右键复制链接）')
    async def pic2pic(self, interaction: discord.Interaction, pic: str):
        try:
            await interaction.response.defer(ephemeral=True)
            picembed = get_picinfo(pic)
            await Paginator.Simple(timeout=3600).start(interaction, pages=picembed)

        except Exception as e:
            print(e)


async def setup(client):
    await client.add_cog(Pic2Pic(client))
