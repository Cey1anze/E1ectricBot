import json

import requests
import discord
from discord.ext import commands
from discord import app_commands
from Basic_bot.Core.init_cog import InitCog


def get_weather(city):
    try:
        url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{}/today?unitGroup=metric&key=your_key&contentType=json".format(
            city)
        r = requests.get(url)
        result = r.json()

        print(type(result))

        city = result["address"]
        timezone = result["timezone"]  # 时区
        datetime = result["days"][0]["datetime"]
        latitude = result["latitude"]  # 经度
        longitude = result["longitude"]  # 维度

        conditions = result["days"][0]["conditions"]  # 天气

        temp = result["days"][0]["temp"]  # 温度
        pressure = result["days"][0]["pressure"]  # 气压
        humidity = result["days"][0]["humidity"]  # 湿度
        temp_min = result["days"][0]["tempmin"]  # 最低温度
        temp_max = result["days"][0]["tempmax"]  # 最高温度
        feelslikemax = result["days"][0]["feelslikemax"]  # 体感最高温度
        feelslikemin = result["days"][0]["feelslikemin"]  # 体感最低温度
        visibility = result["days"][0]["visibility"]  # 能见度
        windspeed = result["days"][0]["windspeed"]  # 风速

        sunrise = result["days"][0]["sunrise"]  # 日出
        sunset = result["days"][0]["sunset"]  # 日落

        embed = discord.Embed(title=f'{city}', description=f'{city} 的天气情况', color=0x388ce5)
        embed.set_thumbnail(url='https://cdn-icons-png.flaticon.com/512/5483/5483481.png')
        embed.add_field(name="天气情况", value=f'{conditions}', inline=True)
        embed.add_field(name="气压", value=f'{pressure} 百帕', inline=True)
        embed.add_field(name='\u200B', value='\u200B', inline=True)
        embed.add_field(name="湿度", value=f'{humidity} %', inline=True)
        embed.add_field(name="能见度", value=f'{visibility} 公里', inline=True)
        embed.add_field(name='\u200B', value='\u200B', inline=True)
        embed.add_field(name="最高温度", value=f'{temp_max} ℃', inline=True)
        embed.add_field(name="最低气温", value=f'{temp_min} ℃', inline=True)
        embed.add_field(name='\u200B', value='\u200B', inline=True)
        embed.add_field(name="体感最高温度", value=f'{feelslikemax} ℃', inline=True)
        embed.add_field(name="体感最低温度", value=f'{feelslikemin} ℃', inline=True)
        embed.add_field(name='\u200B', value='\u200B', inline=True)
        embed.add_field(name="日出时间", value=sunrise, inline=True)
        embed.add_field(name="日落时间", value=sunset, inline=True)
        embed.set_footer(text=f'日期：{datetime} , 时区：{timezone} , 经度：{latitude} , 维度：{longitude}')
        return embed

    except Exception as e:
        print(e)
        embed = discord.Embed(title="出现错误", color=0x14aaeb)
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/5483/5483481.png")
        embed.add_field(name="Error", value="出错了，请检查输入的内容", inline=True)
        return embed


class Weather(InitCog):
    @app_commands.command(name='weather', description='查询某个城市的天气')
    @app_commands.describe(city='需要查询的城市，国内城市请输入拼音，首字母大写，例：Beijing')
    async def weather(self, interaction: discord.Interaction, city: str):
        embed = get_weather(city)
        await interaction.response.defer()
        await interaction.followup.send(embed=embed)


async def setup(client):
    await client.add_cog(Weather(client))
