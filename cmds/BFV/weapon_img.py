import io
import requests
import discord
from discord import app_commands
from discord.app_commands import Choice
import matplotlib.pyplot as plt
from Core.init_cog import InitCog

kill_data = []
headshot_data = []
accuracy_data = []
kpm_data = []
data = None


def get_img(name, platform):
    global kill_data, headshot_data, accuracy_data, kpm_data, data
    del data, kill_data, headshot_data, accuracy_data, kpm_data
    plt.close()
    url = "https://api.gametools.network/bfv/weapons/?format_values=true&name={}&platform={}&skip_battlelog=false&lang=zh-cn".format(
        name, platform)
    r = requests.get(url)
    data = r.json()

    if 'errors' in data:
        if 'Player not found' in data['errors']:
            error_embed = discord.Embed(title='ERROR:玩家名称错误,请检查玩家名称', colour=discord.Colour.red())
            return error_embed
        elif 'Failed to fetch data from source' in data['errors']:
            error_embed = discord.Embed(title='ERROR:获取数据失败', colour=discord.Colour.red())
            return error_embed
        elif 'detail' in data:
            error_embed = discord.Embed(title='ERROR:查询验证失败', colour=discord.Colour.red())
            return error_embed
    else:

        kill_data = sorted(data['weapons'], key=lambda x: x['kills'], reverse=True)
        headshot_data = sorted(data['weapons'], key=lambda x: float(x['headshots'][:-1]), reverse=True)
        accuracy_data = sorted(data['weapons'], key=lambda x: float(x['accuracy'][:-1]), reverse=True)
        kpm_data = sorted(data['weapons'], key=lambda x: float(x['killsPerMinute']), reverse=True)

        # 提取武器名称和杀敌数
        weapon_names = [w['weaponName'] for w in kill_data[:20]]
        kills = [w['kills'] for w in kill_data[:20]]

        weapon_names1 = [w['weaponName'] for w in headshot_data[:20]]
        headshots = [float(w['headshots'][:-1]) for w in headshot_data[:20]]

        weapon_names2 = [w['weaponName'] for w in accuracy_data[:20]]
        accuracy = [float(w['accuracy'][:-1]) for w in accuracy_data[:20]]

        weapon_names3 = [w['weaponName'] for w in kpm_data[:20]]
        kpm = [float(w['killsPerMinute']) for w in kpm_data[:20]]

        params = {
            'figure.figsize': '25,15'
        }
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['figure.facecolor'] = 'black'
        plt.rcParams['text.color'] = 'white'
        plt.rcParams['xtick.color'] = 'white'
        plt.rcParams['ytick.color'] = 'white'
        plt.rcParams.update(params)

        # 生成柱状图
        plt.subplot(221, facecolor='black')
        p1 = plt.bar(weapon_names, kills, width=0.6, label='value')
        plt.bar_label(p1, label_type='edge')
        plt.title('总击杀数 (Top 20)')
        plt.ylabel('击杀数')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        plt.subplot(222, facecolor='black')
        p2 = plt.bar(weapon_names1, headshots, width=0.6, label='value')
        plt.bar_label(p2, label_type='edge', fmt='%.2f%%')
        plt.title('爆头率 (Top 20)')
        plt.ylabel('爆头率')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        plt.subplot(223, facecolor='black')
        p2 = plt.bar(weapon_names2, accuracy, width=0.6, label='value')
        plt.bar_label(p2, label_type='edge', fmt='%.2f%%')
        plt.title('命中率 (Top 20)')
        plt.ylabel('命中率')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        plt.subplot(224, facecolor='black')
        p2 = plt.bar(weapon_names3, kpm, width=0.6, label='value')
        plt.bar_label(p2, label_type='edge')
        plt.title('KPM (Top 20)')
        plt.ylabel('KPM')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)

        return buf


class Weapon(InitCog):

    @app_commands.command(name='bfv-weapon', description='查询玩家的武器数据(图表)-按顺序查询,耐心等待')
    @app_commands.describe(name='需要查询玩家的名称，即游戏内名称')
    @app_commands.rename(option='游玩平台')
    @app_commands.choices(option=[
        Choice(name='PC', value='pc'),
        Choice(name='PlayStation', value='ps4'),
        Choice(name='XBOX ONE', value='xboxone')])
    async def weapon(self, interaction: discord.Interaction, option: str, name: str):
        global data
        await interaction.response.defer()
        try:
            result = get_img(name, platform=option)
            if isinstance(result, discord.Embed):
                await interaction.followup.send(embed=result)
            elif isinstance(result, io.BytesIO):
                await interaction.followup.send(f'请看下面图表⬇{interaction.user.mention}',
                                                file=discord.File(result, 'data.png'))

        except Exception as e:
            print(e)


async def setup(client):
    await client.add_cog(Weapon(client))
