import discord
from discord.ext import commands
from Basic_bot.Core.init_cog import InitCog



class Test(InitCog):

    @commands.command(name='ping', help='测试机器人延迟')
    async def ping(self, ctx):
        await ctx.channel.purge(limit=1)
        await ctx.send(embed=discord.Embed(description=f'🕒延迟：{round(self.client.latency * 1000)} ms',
                                           colour=discord.Color.from_rgb(130, 156, 242)))


async def setup(client):
    await client.add_cog(Test(client))
