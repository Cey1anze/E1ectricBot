import requests
import discord
from discord.app_commands import Choice
from discord.ext import commands
from discord import app_commands
from Basic_bot.Core.init_cog import InitCog


def get_playerstats(name, platform):
    try:
        url = "https://api.gametools.network/bfv/stats/?format_values=true&name={}&platform={}&skip_battlelog=false&lang=zh-cn".format(
            name, platform)
        r = requests.get(url)
        result = r.json()

        avatar = result['avatar']  # 图像
        username = result['userName']  # 名称
        rank = result['rank']  # 等级
        spm = result['scorePerMinute']  # spm
        kpm = result['killsPerMinute']  # kpm
        winper = result['winPercent']  # 胜率
        bestclass = result['bestClass']  # 最佳兵种
        accuracy = result['accuracy']  # 命中率
        headshots = result['headshots']  # 爆头率
        headShots = result['headShots']
        secondsPlayed = result['secondsPlayed']  # 游玩时间
        killDeath = result['killDeath']  # kd
        kills = result['kills']  # 击杀数
        deaths = result['deaths']  # 死亡数
        wins = result['wins']  # 胜场
        loses = result['loses']  # 输场
        longestHeadShot = result['longestHeadShot']  # 最长爆头距离
        revives = result['revives']  # 复活数
        highestKillStreak = result['highestKillStreak']  # 最高连杀
        roundsPlayed = result['roundsPlayed']  # 游玩回合数
        awardScore = result['awardScore']  # 总分

        embed = discord.Embed(title="详细信息戳我",
                              url="https://gametools.network/stats/{}/name/{}?game=bfv".format(platform, name),
                              description=f"等级：{rank} , 游玩时间：{round(secondsPlayed / 3600)} h")
        embed.set_author(name=f"{username}的游戏信息")
        embed.set_thumbnail(url=avatar)
        embed.add_field(name="K/D", value=killDeath, inline=True)
        embed.add_field(name="胜率", value=winper, inline=True)
        embed.add_field(name='\u200B', value='\u200B', inline=True)
        embed.add_field(name="SPM（每分钟得分）", value=spm, inline=True)
        embed.add_field(name="KPM（每分钟击杀）", value=kpm, inline=True)
        embed.add_field(name='\u200B', value='\u200B', inline=True)
        embed.add_field(name="击杀数", value=kills, inline=True)
        embed.add_field(name="死亡数", value=deaths, inline=True)
        embed.add_field(name='\u200B', value='\u200B', inline=True)
        embed.add_field(name="爆头数", value=headShots, inline=True)
        embed.add_field(name="爆头率", value=headshots, inline=True)
        embed.add_field(name='\u200B', value='\u200B', inline=True)
        embed.add_field(name="复活次数", value=int(revives), inline=True)
        embed.add_field(name="命中率", value=accuracy, inline=True)
        embed.add_field(name='\u200B', value='\u200B', inline=True)
        embed.add_field(name="胜利场数", value=wins, inline=True)
        embed.add_field(name="失败场数", value=loses, inline=True)
        embed.add_field(name='\u200B', value='\u200B', inline=True)
        embed.add_field(name="最高连杀", value=highestKillStreak, inline=True)
        embed.add_field(name="最远爆头距离", value=f'{int(longestHeadShot)} m', inline=True)
        embed.add_field(name='\u200B', value='\u200B', inline=True)
        embed.add_field(name="游玩回合数", value=roundsPlayed, inline=True)
        embed.add_field(name="总获得分数", value=int(awardScore), inline=True)
        embed.add_field(name='\u200B', value='\u200B', inline=True)
        embed.add_field(name="最佳兵种", value=bestclass, inline=True)
        return embed

    except Exception as e:
        print(e)
        embed = discord.Embed(title="出现错误", color=0x14aaeb)
        embed.add_field(name="Error", value="出错了，请检查输入的内容", inline=True)
        return embed


class Playerstats(InitCog):
    @app_commands.command(name='playerstats', description='查询某个玩家的信息')
    @app_commands.describe(name='需要查询玩家的名称，即游戏内名称')
    @app_commands.rename(option='游玩平台')
    @app_commands.choices(option=[
        Choice(name='PC', value=0),
        Choice(name='PlayStation', value=1),
        Choice(name='XBOX ONE', value=2)])
    async def playerstats(self, interaction: discord.Interaction, option: int, name: str):
        if option == 0:
            embed = get_playerstats(name, platform='pc')
            await interaction.response.defer()
            await interaction.followup.send(embed=embed)
        elif option == 1:
            embed = get_playerstats(name, platform='ps4')
            await interaction.response.defer()
            await interaction.followup.send(embed=embed)
        elif option == 2:
            embed = get_playerstats(name, platform='xboxone')
            await interaction.response.defer()
            await interaction.followup.send(embed=embed)


async def setup(client):
    await client.add_cog(Playerstats(client))
