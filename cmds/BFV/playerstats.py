import discord
import requests
from discord import app_commands
from discord.app_commands import Choice

from Core.init_cog import InitCog

plane_names = []
plane_kills = []
plane_time = []

tank_names = []
tank_kills = []
tank_time = []

trans_names = []
trans_kills = []
trans_time = []

plane_names.clear()
plane_kills.clear()
plane_time.clear()

tank_names.clear()
tank_kills.clear()
tank_time.clear()

trans_names.clear()
trans_kills.clear()
trans_time.clear()

name, platform = None, None


def get_playerstats():
    global name, platform
    url1 = "https://api.gametools.network/bfban/checkban?names={}".format(name)
    r1 = requests.get(url1)
    banresult = r1.json()

    url = "https://api.gametools.network/bfv/stats/?format_values=true&name={}&platform={}&skip_battlelog=false&lang=zh-cn".format(
        name, platform)
    r = requests.get(url)
    result = r.json()
    try:

        if 'errors' in result:
            http404embed = discord.Embed(title='返回结果', color=0xf44336)
            http404embed.add_field(name='Error', value=f'检查输入的名称，当前输入的名称为 `{name}`', inline=False)
            return http404embed
        elif "detail" in result:
            http422embed = discord.Embed(title="返回结果", color=0xf44336).add_field(name="Error", value="接口暂时无法使用",
                                                                                 inline=False)
            return http422embed
        else:

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
            checkban = banresult['names'][f'{name}'.lower()]['hacker']

            if not checkban:
                ban = ' 🟢 无异常'
            else:
                ban = ' 🔴 石锤'

            embed = discord.Embed(title="详细信息戳我",
                                  url="https://gametools.network/stats/{}/name/{}?game=bfv".format(platform, name),
                                  description=f"等级 : {rank} , 游玩时间 : {round(secondsPlayed / 3600)} h , 联Ban查询 :{ban}")
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
            embed.add_field(name="急救次数", value=int(revives), inline=True)
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
        return discord.Embed(title="查询失败", description=f"错误信息：{e}", colour=0xf44336)


def get_vehicles():
    global name, platform
    url = "https://api.gametools.network/bfv/vehicles/?name={}&platform={}&skip_battlelog=false&lang=zh-cn".format(
        name, platform)
    r = requests.get(url)
    result = r.json()

    try:
        if 'errors' in result:
            if 'playername not found' in result['errors']:
                error_embed = discord.Embed(title='玩家名称错误', colour=discord.Colour.red())
                return error_embed
            elif 'Failed to fetch data from source' in result['errors']:
                error_embed = discord.Embed(title='获取数据失败', colour=discord.Colour.red())
                return error_embed
            elif 'detail' in result:
                error_embed = discord.Embed(title='查询验证失败', colour=discord.Colour.red())
                return error_embed
        else:
            for vehicles in result['vehicles']:
                if vehicles['type'] == '飞机':
                    plane_names.append(vehicles['vehicleName'])
                    plane_kills.append(vehicles['kills'])
                    plane_time.append(vehicles['timeIn'])
                if vehicles['type'] == '坦克':
                    tank_names.append(vehicles['vehicleName'])
                    tank_kills.append(vehicles['kills'])
                    tank_time.append(vehicles['timeIn'])
                if vehicles['type'] == '运输载具':
                    trans_names.append(vehicles['vehicleName'])
                    trans_kills.append(vehicles['kills'])
                    trans_time.append(vehicles['timeIn'])

        plane_embed = discord.Embed(title='飞机数据', colour=discord.Colour.green())
        tank_embed = discord.Embed(title='坦克数据', colour=discord.Colour.green())
        trans_embed = discord.Embed(title='运输载具数据', colour=discord.Colour.green())
        for i in range(len(plane_names)):
            plane_embed.add_field(name=f'{plane_names[i]}',
                                  value=f'☠击杀：{plane_kills[i]}\n⏱游玩时间：{round(plane_time[i] / 3600)}h')
        for i in range(len(tank_names)):
            tank_embed.add_field(name=f'{tank_names[i]}',
                                 value=f'☠击杀：{tank_kills[i]}\n⏱游玩时间：{round(tank_time[i] / 3600)}h')
        for i in range(len(trans_names)):
            trans_embed.add_field(name=f'{trans_names[i]}',
                                  value=f'☠击杀：{trans_kills[i]}\n⏱游玩时间：{round(trans_time[i] / 3600)}h')

        plane_names.clear()
        plane_kills.clear()
        plane_time.clear()

        tank_names.clear()
        tank_kills.clear()
        tank_time.clear()

        trans_names.clear()
        trans_kills.clear()
        trans_time.clear()
        
        return plane_embed, tank_embed, trans_embed
    except Exception as e:
        return discord.Embed(title="异常错误", description=f"错误信息：{e}", colour=0xf44336)


class Button(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.plane = discord.ui.Button(label="飞机数据", style=discord.ButtonStyle.success)
        self.tank = discord.ui.Button(label="坦克数据", style=discord.ButtonStyle.success)
        self.trans = discord.ui.Button(label="运输载具数据", style=discord.ButtonStyle.success)
        self.add_item(self.plane)
        self.add_item(self.tank)
        self.add_item(self.trans)
        self.plane.callback = plane
        self.tank.callback = tank
        self.trans.callback = trans


async def plane(interaction: discord.Interaction):
    embeds = get_vehicles()
    if isinstance(embeds, tuple):
        await interaction.response.edit_message(embed=embeds[0])
    else:
        await interaction.response.edit_message(embed=embeds)


async def tank(interaction: discord.Interaction):
    embeds = get_vehicles()
    if isinstance(embeds, tuple):
        await interaction.response.edit_message(embed=embeds[1])
    else:
        await interaction.response.edit_message(embed=embeds)


async def trans(interaction: discord.Interaction):
    embeds = get_vehicles()
    if isinstance(embeds, tuple):
        await interaction.response.edit_message(embed=embeds[2])
    else:
        await interaction.response.edit_message(embed=embeds)


class Playerstats(InitCog):
    @app_commands.command(name='bfv-playerstats', description='查询某个玩家的信息')
    @app_commands.describe(playername='需要查询玩家的名称，即游戏内名称')
    @app_commands.rename(option='游玩平台')
    @app_commands.choices(option=[
        Choice(name='PC', value='pc'),
        Choice(name='PlayStation', value='ps4'),
        Choice(name='XBOX ONE', value='xboxone')])
    async def playerstats(self, interaction: discord.Interaction, option: str, playername: str):
        global name, platform
        try:
            name = playername
            platform = option
            view = Button()
            await interaction.response.defer()
            await interaction.followup.send(embed=get_playerstats(), view=view)
        except Exception as e:
            print(e)


async def setup(client):
    await client.add_cog(Playerstats(client))
