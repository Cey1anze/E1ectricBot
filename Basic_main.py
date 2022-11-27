import asyncio
import discord
import os
from discord.ext import commands
from Basic_bot.Core import loadjson

jdata = loadjson.load_mainconfig()

client = commands.Bot(command_prefix='?', intents=discord.Intents.all())


# read cogs from cmds and load them
async def setup_hook():
    for Filename in os.listdir('./cmds'):
        if Filename.endswith('.py'):
            await client.load_extension(f'cmds.{Filename[:-3]}')


@client.command(name='load', help='load cogs')
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


@client.command(name='unload', help='unload cogs')
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


@client.command(name='reload', help='reload cogs')
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


@client.event
async def on_ready():
    print(f"bot logged as {client.user}")


async def main():
    await setup_hook()
    await client.start(jdata['Token'])


asyncio.run(main())