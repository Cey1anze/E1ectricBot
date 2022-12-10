import asyncio
import discord
import os
from discord.ext import commands
from Basic_bot.Core import loadjson
from Basic_bot.cmds.GPT import responses

jdata = loadjson.load_mainconfig()
helpguide = loadjson.load_helpconfig()
GPTbot = loadjson.load_chatconfig()
client = commands.Bot(command_prefix='?', intents=discord.Intents.all())
is_private = False


# read cogs from cmds and load them
async def setup_hook():
    for Filename in os.listdir('./cmds'):
        if Filename.endswith('.py'):
            await client.load_extension(f'cmds.{Filename[:-3]}')


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


async def send_message(message, user_message):
    await message.response.defer(ephemeral=is_private)
    try:
        response = '> **' + user_message + '** - <@' + str(message.user.id) + '>\n\n' + responses.handle_response(
            user_message)
        if len(response) > 1900:
            # Split the response into smaller chunks of no more than 1900 characters each(Discord limit is 2000 per chunk)
            response_chunks = [response[i:i + 1900]
                               for i in range(0, len(response), 1900)]
            for chunk in response_chunks:
                await message.followup.send(chunk)
        else:
            await message.followup.send(response)
    except Exception as e:
        await message.followup.send("> **Error: There are something went wrong. Please try again later!**")
        print(e)


@client.tree.command(name="chat", description="与chatGPT聊天")
async def chat(interaction: discord.Interaction, *, message: str):
    if interaction.user == client.user:
        return
    username = str(interaction.user)
    user_message = message
    channel = str(interaction.channel)
    print(f"{username} said: '{user_message}' ({channel})")
    await send_message(interaction, user_message)


@client.tree.command(name="private", description="切换为仅自己可见")
async def private(interaction: discord.Interaction):
    global is_private
    await interaction.response.defer(ephemeral=False)
    if not is_private:
        is_private = not is_private
        print("Switch to private mode")
        await interaction.followup.send(
            "> **Info: Next, the response will be sent via private message. If you want to switch back to public mode, use `/public`**")
    else:
        print("You already on private mode!")
        await interaction.followup.send(
            "> **Warn: You already on private mode. If you want to switch to public mode, use `/public`**")


@client.tree.command(name="public", description="切换为所有人可见")
async def public(interaction: discord.Interaction):
    global is_private
    await interaction.response.defer(ephemeral=False)
    if is_private:
        is_private = not is_private
        await interaction.followup.send(
            "> **Info: Next, the response will be sent to the channel directly. If you want to switch back to private mode, use `/private`**")
        print("Switch to public mode")
    else:
        await interaction.followup.send(
            "> **Warn: You already on public mode. If you want to switch to private mode, use `/private`**")
        print("You already on public mode!")


@client.tree.command(name="reset", description="Complete reset gptChat conversation history")
async def reset(interaction: discord.Interaction):
    responses.chatbot.reset_chat()
    await interaction.response.defer(ephemeral=False)
    await interaction.followup.send("> **Info: I have forgotten everything.**")
    print("The CHAT BOT has been successfully reset")


@client.event
async def on_ready():
    sync = await client.tree.sync()
    print(f"bot logged as {client.user}")
    print(f'synced {len(sync)} commands')


async def main():
    await setup_hook()
    await client.start(jdata['Token'])


if __name__ == "__main__":
    asyncio.run(main())
# if you want bot hosting 24/7,dis-annotated next line,and put whole program into replit
# keep_alive()
