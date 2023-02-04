import base64

import Paginator
import discord
import requests
from discord import app_commands
from lxml import etree

from Basic_bot.Core.init_cog import InitCog

base_url = "aHR0cHM6Ly9zdG9yZS5zdGVhbXBvd2VyZWQuY29tL3NlYXJjaC8/c3BlY2lhbHM9MQ=="
url = base64.b64decode(base_url).decode()

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/85.0.4183.102 Safari/537.36', 'Accept-Language': 'zh-CN '}


def get_info():
    global link, img, r, date
    for i in range(10):
        try:
            r = requests.get(url, headers=headers, timeout=8)
            break
        except:
            print("网络连接不太好，请等待...")
            if i == 9:
                print("网络连接失败，程序已终止...")
                raise
            continue

    html = etree.HTML(r.text)

    div = html.xpath("//div[@class='responsive_search_name_combined']")
    div2 = html.xpath("//div[@id='search_resultsRows']")

    text = ""

    titlelist = []
    discountlist = []
    pricelist = []
    newpricelist = []
    summarylist = []
    linklist = []
    imglist = []
    page = {}
    titlelist.clear()
    discountlist.clear()
    pricelist.clear()
    newpricelist.clear()
    summarylist.clear()
    linklist.clear()
    imglist.clear()

    for i in div:
        title = i.xpath(".//span[@class='title']/text()")[0]

        if not len(i.xpath(".//div[@class='col search_discount responsive_secondrow']/span/text()")):
            continue
        titlelist.append(title)

        summary = i.xpath(
            ".//div[@class='col search_reviewscore responsive_secondrow']/span[@class='search_review_summary "
            "positive']/@data-tooltip-html")
        summarylist.append(summary)

        discount = i.xpath(".//div[@class='col search_discount responsive_secondrow']/span/text()")[0]
        discountlist.append(discount)

        price = i.xpath(".//div[@class='col search_price discounted responsive_secondrow']/span/strike/text()")[0]
        pricelist.append(price)

        new_price = i.xpath(".//div[@class='col search_price discounted responsive_secondrow']/text()")[1].strip()
        newpricelist.append(new_price)

    for i in div2:
        link = i.xpath("./a/@href")
        img = i.xpath(".//a/div[@class='col search_capsule']/img/@src")

    # print(len(titlelist))
    # print(len(discountlist))
    # print(len(pricelist))
    # print(len(newpricelist))
    # print(summarylist)
    # print(len(link))
    # print(len(img))

    # Creat Embed
    for i in range(len(titlelist)):
        page[i] = discord.Embed(title=f'{titlelist[i]}', description='此为新加坡区价格，相比于国区更贵', url=f'{link[i]}',
                                colour=0x388ce5)
        page[i].add_field(name="折扣", value=f'{discountlist[i]}', inline=True)
        page[i].add_field(name='\u200B', value='\u200B', inline=True)
        page[i].add_field(name="原价", value=f'{round(float(pricelist[i].replace("S$", "")) * 5.1)} ¥', inline=True)
        page[i].add_field(name="现价", value=f'{round(float(newpricelist[i].replace("S$", "")) * 5.1)} ¥', inline=True)
        page[i].add_field(name="评价",
                          value=f'{str(summarylist[i]).replace("<br>", ",").replace("[", "").replace("]", "")}',
                          inline=False)
        page[i].set_image(url=img[i])

    return page


class Steamdiscount(InitCog):
    @app_commands.command(name='steam-discount', description='查询steam正在打折的游戏')
    async def steamdiscount(self, interaction: discord.Interaction):
        try:
            embeds = get_info()
            await Paginator.Simple(timeout=999).start(interaction, pages=embeds)
        except Exception as e:
            print(e)


async def setup(client):
    await client.add_cog(Steamdiscount(client))

# if __name__ == "__main__":
#    get_info()
