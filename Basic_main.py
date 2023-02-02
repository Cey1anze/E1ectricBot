import asyncio
import os

import discord
import wavelink
from discord.ext import commands
from Basic_bot.Core import loadjson
from logs import settings

jdata = loadjson.load_mainconfig()
client = commands.Bot(command_prefix='?', intents=discord.Intents.all())

logger = settings.logging.getLogger("bot")


# read cogs from cmds and load them
async def setup_hook():
    for Filename in os.listdir('./cmds/essentials'):
        if Filename.endswith('.py'):
            await client.load_extension(f'cmds.essentials.{Filename[:-3]}')
    for Filename in os.listdir('./cmds/Music/src/cogs'):
        if Filename.endswith('.py'):
            await client.load_extension(f'cmds.Music.src.cogs.{Filename[:-3]}')
    for Filename in os.listdir('./cmds/BFV'):
        if Filename.endswith('.py'):
            await client.load_extension(f'cmds.BFV.{Filename[:-3]}')
    for Filename in os.listdir('./cmds/chatGPT/src'):
        if Filename.endswith('.py'):
            await client.load_extension(f'cmds.chatGPT.src.{Filename[:-3]}')
    for Filename in os.listdir('./cmds/OtherApicmds'):
        if Filename.endswith('.py'):
            await client.load_extension(f'cmds.OtherApicmds.{Filename[:-3]}')
    for Filename in os.listdir('./cmds/GuildManager'):
        if Filename.endswith('.py'):
            await client.load_extension(f'cmds.GuildManager.{Filename[:-3]}')


@client.command(name='load', help='加载模组')
async def load(ctx, extension):
    try:
        await client.load_extension(f"cmds.{extension}")
        load_embed = discord.Embed(color=discord.Color.from_rgb(130, 156, 242),
                                   description=f"**{extension}** 已成功载入")
        await ctx.send(embed=load_embed)
    except commands.ExtensionNotFound:
        load_embed = discord.Embed(color=discord.Color.from_rgb(130, 156, 242),
                                   description=f"**{extension}** 没有找到")
        await ctx.send(embed=load_embed)
    except commands.ExtensionAlreadyLoaded:
        load_embed = discord.Embed(color=discord.Color.from_rgb(130, 156, 242),
                                   description=f"**{extension}** 已被加载，无需再加载")
        await ctx.send(embed=load_embed)
        return


@client.command(name='unload', help='卸载模组')
async def unload(ctx, extension):
    try:
        await client.unload_extension(f"cmds.{extension}")
        unload_embed = discord.Embed(color=discord.Color.from_rgb(130, 156, 242),
                                     description=f"**{extension}** 已成功卸载")
        await ctx.send(embed=unload_embed)
    except commands.ExtensionNotLoaded:
        unload_embed = discord.Embed(color=discord.Color.from_rgb(130, 156, 242),
                                     description=f"**{extension}** 没有找到 或 已被卸载，无需再次卸载")
        await ctx.send(embed=unload_embed)
        return


@client.command(name='reload', help='重载模组')
async def reload(ctx, extension):
    try:
        await client.reload_extension(f"cmds.{extension}")
        reload_embed = discord.Embed(color=discord.Color.from_rgb(130, 156, 242),
                                     description=f"**{extension}** 已重新载入")
        await ctx.send(embed=reload_embed)
    except commands.ExtensionNotLoaded:
        reload_embed = discord.Embed(color=discord.Color.from_rgb(130, 156, 242),
                                     description=f"**{extension}** 没有找到 或 已被卸载，请先载入")
        await ctx.send(embed=reload_embed)
        return


async def connect_nodes():
    """Connects to the self hosted lavalink server"""
    logger.info("Connecting Nodes")
    await client.wait_until_ready()  ## Wait until the bot is ready.
    await wavelink.NodePool.create_node(
        bot=client,
        host='127.0.0.1',
        port=2333,
        password='YourPasswordHere',
    )  ## Connect to the lavalink server.


@client.event
async def on_ready():
    sync = await client.tree.sync()
    client.loop.create_task(connect_nodes())
    lines = "~~~" * 30
    logger.info(
        "\n%s\n%s is online in %s servers, and is ready to play music\n%s",
        lines,
        client.user,
        len(client.guilds),
        lines,
    )
    print(f"bot logged as {client.user}")
    print(f'synced {len(sync)} commands')


async def main():
    await setup_hook()
    await client.start(jdata['Token'])


if __name__ == "__main__":
    asyncio.run(main())
# if you want bot hosting 24/7,dis-annotated next line,and put whole program into replit
# keep_alive()
