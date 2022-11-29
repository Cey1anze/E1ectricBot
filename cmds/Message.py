import discord
import json
from discord.ext import commands
from Basic_bot.Core.init_cog import InitCog
from Basic_bot.Core.loadjson import load_replyconfig, load_blockwordconfig


class Message(InitCog):

    # clean messages
    @commands.command(name='clean', help='删除若干条消息')
    @commands.is_owner()
    async def clean(self, ctx, num: int):
        await ctx.channel.purge(limit=num + 1)
        await ctx.send(embed=discord.Embed(description=f'已删除 {num} 条消息',
                                           colour=discord.Color.from_rgb(130, 156, 242)))

    # Turn the message sent from bot
    @commands.command(name='resay', help='以机器人方式发送消息')
    @commands.is_owner()
    async def resay(self, ctx, *, msg):
        await ctx.message.delete()
        await ctx.send(msg)

    # Monitor user messages and respond
    @commands.Cog.listener()
    async def on_message(self, msg):
        keyword = load_blockwordconfig()
        # Delete messages with keyword in blockwords(trash words or whatever u want)
        # Lightweight version of Automod, If this function is not required, annotated lines 31-34
        if any(word in msg.content for word in keyword) and msg.author != self.client.user:
            await msg.channel.purge(limit=1)
            await msg.channel.send(embed=discord.Embed(description=f'不要说脏话',
                                                       colour=discord.Color.from_rgb(130, 156, 242)))

        # bot responds after entering specific content
        reply = load_replyconfig()
        reply1 = reply[msg.content]
        if reply is not None and msg.author != self.client.user:
            await msg.channel.send(reply1)

    @commands.command(name='addreply', help='添加自动回复词组')
    @commands.is_owner()
    async def addreply(self, ctx, msg: str, *, answer: str):
        new_data = {msg: answer}

        with open("./configs/replyDict.json", "r", encoding="utf-8") as f:
            old_data = json.load(f)
            old_data.update(new_data)
        with open("./configs/replyDict.json", "w", encoding="utf-8") as f:
            json.dump(old_data, f)

        load_replyconfig()
        await ctx.send(embed=discord.Embed(description=f'已添加自动回复词组： 键入{msg}，回复{answer} ',
                                           colour=discord.Colour.from_rgb(130, 156, 242)))

    @commands.command(name='addblock', help='添加屏蔽词组')
    @commands.is_owner()
    async def addblock(self, ctx, *, msg: str):
        new_data = {msg: msg}

        with open("./configs/blockwords.json", "r", encoding="utf-8") as f:
            old_data = json.load(f)
            old_data.update(new_data)
        with open("./configs/blockwords.json", "w", encoding="utf-8") as f:
            json.dump(old_data, f)

        load_blockwordconfig()
        await ctx.send(embed=discord.Embed(description=f'已添加屏蔽词组： {msg} ',
                                           colour=discord.Colour.from_rgb(130, 156, 242)))


async def setup(client):
    await client.add_cog(Message(client))
