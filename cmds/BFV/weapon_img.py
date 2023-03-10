import io
import requests
import discord
from discord import app_commands
from discord.app_commands import Choice

import matplotlib.pyplot as plt

from Core.init_cog import InitCog


def get_img(name, platform):
    url = "https://api.gametools.network/bfv/weapons/?format_values=true&name={}&platform={}&skip_battlelog=false&lang=zh-cn".format(
        name, platform)
    r = requests.get(url)
    data = r.json()

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
    plt.rcParams.update(params)

    # 生成柱状图
    plt.subplot(221)
    p1 = plt.bar(weapon_names, kills, width=0.6, label='value')
    plt.bar_label(p1, label_type='edge')
    plt.title('总击杀数 (Top 20)')
    plt.ylabel('击杀数')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    plt.subplot(222)
    p2 = plt.bar(weapon_names1, headshots, width=0.6, label='value')
    plt.bar_label(p2, label_type='edge', fmt='%.2f%%')
    plt.title('爆头率 (Top 20)')
    plt.ylabel('爆头率')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    plt.subplot(223)
    p2 = plt.bar(weapon_names2, accuracy, width=0.6, label='value')
    plt.bar_label(p2, label_type='edge', fmt='%.2f%%')
    plt.title('命中率 (Top 20)')
    plt.ylabel('命中率')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    plt.subplot(224)
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

    @app_commands.command(name='bfv-weapon', description='查询玩家的武器数据')
    @app_commands.describe(name='需要查询玩家的名称，即游戏内名称')
    @app_commands.rename(option='游玩平台')
    @app_commands.choices(option=[
        Choice(name='PC', value='pc'),
        Choice(name='PlayStation', value='ps4'),
        Choice(name='XBOX ONE', value='xboxone')])
    async def weapon(self, interaction: discord.Interaction, option: str, name: str):
        await interaction.response.defer()
        data = get_img(name, platform=option)
        await interaction.followup.send('请看下面图表⬇')
        await interaction.channel.send(file=discord.File(data, 'data.png'))


async def setup(client):
    await client.add_cog(Weapon(client))
