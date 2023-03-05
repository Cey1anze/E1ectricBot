import discord
from discord import app_commands
from Basic_main import client
from Core.init_cog import InitCog
from Basic_bot.cmds.chatGPT import responses
from Core import loadjson

config = loadjson.load_chatconfig()

isPrivate = False
chat_model = 'OFFICIAL'


async def send_message(message, user_message):
    author = message.user.id
    await message.response.defer(ephemeral=isPrivate)
    try:
        response = '> **' + user_message + '** - <@' + \
                   str(author) + '> \n\n'
        if chat_model == "OFFICIAL":
            response = f"{response}{await responses.official_handle_response(user_message)}"
        elif chat_model == "UNOFFICIAL":
            response = f"{response}{await responses.unofficial_handle_response(user_message)}"
        char_limit = 1900
        if len(response) > char_limit:
            if "```" in response:
                parts = response.split("```")

                for i in range(0, len(parts)):
                    if i % 2 == 0:
                        await message.followup.send(parts[i])

                    else:
                        code_block = parts[i].split("\n")
                        formatted_code_block = ""
                        for line in code_block:
                            while len(line) > char_limit:
                                # Split the line at the 50th character
                                formatted_code_block += line[:char_limit] + "\n"
                                line = line[char_limit:]
                            formatted_code_block += line + "\n"

                        if (len(formatted_code_block) > char_limit + 100):
                            code_block_chunks = [formatted_code_block[i:i + char_limit]
                                                 for i in range(0, len(formatted_code_block), char_limit)]
                            for chunk in code_block_chunks:
                                await message.followup.send("```" + chunk + "```")
                        else:
                            await message.followup.send("```" + formatted_code_block + "```")

            else:
                response_chunks = [response[i:i + char_limit]
                                   for i in range(0, len(response), char_limit)]
                for chunk in response_chunks:
                    await message.followup.send(chunk)
        else:
            await message.followup.send(response)
    except Exception:
        await message.followup.send("> **Error: 出现错误, 请稍后重试!**")


class Chat(InitCog):

    @app_commands.command(name="chatgpt-chat", description="和ChatGPT聊天吧")
    async def chat(self, interaction: discord.Interaction, *, message: str):
        if interaction.user == client.user:
            return
        username = str(interaction.user)
        user_message = message
        channel = str(interaction.channel)
        await send_message(interaction, user_message)

    @app_commands.command(name="chatgpt-private", description="将回复信息转为仅自己可见")
    async def private(self, interaction: discord.Interaction):
        global isPrivate
        await interaction.response.defer(ephemeral=False)
        if not isPrivate:
            isPrivate = not isPrivate
            await interaction.followup.send(
                "> **Info: 接下来, 机器人将通过私人模式发送响应。如果要切换回公共模式, 请使用 `/public`**")
        else:
            await interaction.followup.send(
                "> **Warn: 你已经进入私人模式了。如果你想切换到公共模式, 请使用 `/public`**")

    @app_commands.command(name="chatgpt-public", description="将回复信息转为所有人可见")
    async def public(self, interaction: discord.Interaction):
        global isPrivate
        await interaction.response.defer(ephemeral=False)
        if isPrivate:
            isPrivate = not isPrivate
            await interaction.followup.send(
                "> **Info: 接下来, 响应将直接发送到频道。如果你想切换回私有模式, 请使用 `/private`**")
        else:
            await interaction.followup.send(
                "> **Warn: 你已经进入公共模式了。如果你想切换到私有模式, 请使用 `/private`**")

    @app_commands.command(name="chatgpt-model", description="切换chatGPT引擎")
    @app_commands.choices(choices=[
        app_commands.Choice(name="Official GPT-3.5", value="OFFICIAL"),
        app_commands.Choice(name="Website ChatGPT", value="UNOFFCIAL")
    ])
    async def chat_model(self, interaction: discord.Interaction, choices: app_commands.Choice[str]):
        global chat_model
        await interaction.response.defer(ephemeral=False)
        if choices.value == "OFFICIAL":
            chat_model = "OFFICIAL"
            await interaction.followup.send(
                "> **Info: 你现在正在使用付费版GPT-3.5模型。**")
        elif choices.value == "UNOFFCIAL":
            chat_model = "UNOFFICIAL"
            await interaction.followup.send(
                "> **Info: 你正在使用免费版网页chatGPT。**")

    @app_commands.command(name="chatgpt-reset", description="清理chatGPT历史记录")
    async def reset(self, interaction: discord.Interaction):
        if chat_model == "OFFICIAL":
            responses.offical_chatbot.reset()
        elif chat_model == "UNOFFICIAL":
            responses.unofficial_chatbot.reset_chat()
        await interaction.response.defer(ephemeral=False)
        await interaction.followup.send("> **Info: 已完成清理。**")


async def setup(client):
    await client.add_cog(Chat(client))
