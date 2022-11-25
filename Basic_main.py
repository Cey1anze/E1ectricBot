import asyncio
import discord
import os
from discord.ext import commands
from Basic_bot.Core import loadjson

jdata = loadjson.load()

client = commands.Bot(command_prefix='?', intents=discord.Intents.all())


async def setup_hook():
    for Filename in os.listdir('./cmds'):
        if Filename.endswith('.py'):
            await client.load_extension(f'cmds.{Filename[:-3]}')


@client.command(name='load', help='load cogs')
async def load(ctx, extension):
    await client.load_extension(f'cmds.{extension}')
    await ctx.send(f'{extension} loaded')


@client.command(name='unload', help='unload cogs')
async def unload(ctx, extension):
    await client.unload_extension(f'cmds.{extension}')
    await ctx.send(f'{extension} unloaded')


@client.command(name='reload', help='reload cogs')
async def reload(ctx, extension):
    await client.reload_extension(f'cmds.{extension}')
    await ctx.send(f'{extension} re-loaded')


@client.event
async def on_ready():
    print(f"bot logged as {client.user}")


async def main():
    await setup_hook()
    await client.start(jdata['Token'])


asyncio.run(main())
