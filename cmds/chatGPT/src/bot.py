import os

import discord
import openai
from random import randrange
from discord import app_commands

from Core import loadjson
from Core.init_cog import InitCog
from cmds.chatGPT import responses, art, personas

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
        if interaction.user == self.client.user:
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
                "> **Info: 接下来, 响应将仅自己可见。如需切换回公共模式, 请使用 `/public`**")
        else:
            await interaction.followup.send(
                "> **Warn: 你已进入私人模式。如需切换到公共模式, 请使用 `/public`**")

    @app_commands.command(name="chatgpt-public", description="将回复信息转为所有人可见")
    async def public(self, interaction: discord.Interaction):
        global isPrivate
        await interaction.response.defer(ephemeral=False)
        if isPrivate:
            isPrivate = not isPrivate
            await interaction.followup.send(
                "> **Info: 接下来, 响应将会被所有人可见。如需切换回私人模式, 请使用 `/private`**")
        else:
            await interaction.followup.send(
                "> **Warn: 你已进入公共模式。如需切换回私人模式, 请使用 `/private`**")

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
                "> **Info: 你现在正在使用付费版**")
        elif choices.value == "UNOFFCIAL":
            chat_model = "UNOFFICIAL"
            await interaction.followup.send(
                "> **Info: 你正在使用免费版**")

    @app_commands.command(name="chatgpt-reset", description="清理chatGPT历史记录")
    async def reset(self, interaction: discord.Interaction):
        if chat_model == "OFFICIAL":
            responses.chatbot.reset()
        elif chat_model == "UNOFFICIAL":
            responses.chatbot.reset_chat()
        await interaction.response.defer(ephemeral=False)
        await interaction.followup.send("> **Info: 已完成清理。**")

    @app_commands.command(name="chatgpt-draw", description="使用Dalle2模型生成图像")
    async def draw(self, interaction: discord.Interaction, *, prompt: str):
        if interaction.user == self.client.user:
            return

        # await interaction.response.defer(ephemeral=False)
        username = str(interaction.user)
        channel = str(interaction.channel)

        await interaction.response.defer(thinking=True)
        try:
            img = await art.draw(prompt)

            file = discord.File(img, filename="image.png")
            title = '> **' + prompt + '**\n'
            embed = discord.Embed(title=title)
            embed.set_image(url="attachment://image.png")

            # send image in an embed
            await interaction.followup.send(file=file, embed=embed)

            file.close()
            os.remove(img)

        except openai.InvalidRequestError:
            await interaction.followup.send(
                "> **Warn: 请求错误 😿**")

        except Exception as e:
            await interaction.followup.send(
                "> **Warn: 出错了 😿**")

    @app_commands.command(name="chatgpt-switchpersona",
                          description="在可选的chatGPT'越狱模型'之间切换,使用某些角色可能产生粗俗或令人不安的内容。使用时请自行承担风险!!!")
    @app_commands.choices(persona=[
        app_commands.Choice(name="Random", value="random"),
        app_commands.Choice(name="Standard", value="standard"),
        app_commands.Choice(name="Do Anything Now 11.0", value="dan"),
        app_commands.Choice(name="Superior Do Anything", value="sda"),
        app_commands.Choice(name="Evil Confidant", value="confidant"),
        app_commands.Choice(name="BasedGPT v2", value="based"),
        app_commands.Choice(name="OPPO", value="oppo"),
        app_commands.Choice(name="Developer Mode v2", value="dev")
    ])
    async def switch(self, interaction: discord.Interaction, persona: app_commands.Choice[str]):
        if interaction.user == self.client.user:
            return

        await interaction.response.defer(thinking=True)
        username = str(interaction.user)
        channel = str(interaction.channel)

        persona = persona.value

        if persona == personas.current_persona:
            await interaction.followup.send(f"> **Warn: 当前为 `{persona}` 角色，无需再次切换**")

        elif persona == "standard":
            chat_model = config["CHAT_MODEL"]
            if chat_model == "OFFICIAL":
                responses.chatbot.reset()
            elif chat_model == "UNOFFICIAL":
                responses.chatbot.reset_chat()

            personas.current_persona = "standard"
            await interaction.followup.send(
                f"> **Info: 已切换至 `{persona}` 角色**")

        elif persona == "random":
            choices = list(personas.PERSONAS.keys())
            choice = randrange(0, 6)
            chosen_persona = choices[choice]
            personas.current_persona = chosen_persona
            await responses.switch_persona(chosen_persona)
            await interaction.followup.send(
                f"> **Info: 已切换至 `{chosen_persona}` 角色**")

        elif persona in personas.PERSONAS:
            try:
                await responses.switch_persona(persona)
                personas.current_persona = persona
                await interaction.followup.send(
                    f"> **Info: 已切换至 `{persona}` 角色**")
            except Exception as e:
                await interaction.followup.send(
                    "> **Error: 出了点问题，请稍后再试! 😿**")

        else:
            await interaction.followup.send(
                f"> **Error: 没有可用的角色: `{persona}` 😿**")


async def setup(client):
    await client.add_cog(Chat(client))
