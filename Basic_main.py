import asyncio
import json
import discord
import os
from discord.ext import commands

with open('./config.json', 'r', encoding='UTF-8') as jf:
    jdata = json.load(jf)

client = commands.Bot(command_prefix='?', intents=discord.Intents.all())


async def setup_hook():
    for Filename in os.listdir('./cmds'):
        if Filename.endswith('.py'):
            await client.load_extension(f'cmds.{Filename[:-3]}')


@client.event
async def on_ready():
    print(f"bot logged as {client.user}")


async def main():
    await setup_hook()
    await client.start(jdata['Token'])


asyncio.run(main())
