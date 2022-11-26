import discord
from discord.ext import commands
from Basic_bot.Core.init_cog import InitCog
from Basic_bot.Core.loadjson import load_replyconfig, load_blockwordconfig

keyword = load_blockwordconfig()
reply = load_replyconfig()


class Message(InitCog):

    # clean messages
    @commands.command(name='clean', help='Delete a specific number of messages')
    async def clean(self, ctx, num: int):
        await ctx.channel.purge(limit=num + 1)
        await ctx.send(f'{num} 条消息已被删除')

    # Turn the message sent from bot
    @commands.command(name='resay', help='Sending messages as robots')
    async def resay(self, ctx, *, msg):
        await ctx.message.delete()
        await ctx.send(msg)

    # Monitor user messages and respond
    @commands.Cog.listener()
    async def on_message(self, msg):
        # Delete messages with keyword in blockwords(trash words or whatever u want)
        if any(word in msg.content for word in keyword) and msg.author != self.client.user:
            await msg.channel.purge(limit=1)
            await msg.channel.send(f'不要说垃圾话')

        # bot responds after entering specific content
        reply1 = reply[msg.content]
        if reply is not None and msg.author != self.client.user:
            await msg.channel.send(reply1)


async def setup(client):
    await client.add_cog(Message(client))
