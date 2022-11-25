import discord
from discord.ext import commands
from Basic_bot.Core.init_cog import InitCog


class Message(InitCog):

    @commands.command(name='clean', help='Delete a specific number of messages')
    async def clean(self, ctx, num: int):
        await ctx.channel.purge(limit=num + 1)
        await ctx.send(f'{num} messages deleted')

    @commands.command(name='resay', help='Sending messages as robots')
    async def resay(self, ctx, *, msg):
        await ctx.message.delete()
        await ctx.send(msg)


async def setup(client):
    await client.add_cog(Message(client))
