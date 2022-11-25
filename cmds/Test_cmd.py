import discord
from discord.ext import commands
from Basic_bot.Core.init_cog import InitCog


class Test(InitCog):

    @commands.command(name='ping', help='Test bot delay')
    async def ping(self, ctx):
        await ctx.send(f'机器人延迟：{round(self.client.latency * 1000)}ms')


async def setup(client):
    await client.add_cog(Test(client))
