import discord
from discord import app_commands

from Basic_bot.cmds.chatGPT import responses
from Core import loadjson
from Core.init_cog import InitCog

config = loadjson.load_chatconfig()

isPrivate = False


async def send_message(message, user_message):
    await message.response.defer(ephemeral=isPrivate)
    try:
        response = '> **' + user_message + '** - <@' + \
                   str(message.user.id) + '>\n\n'
        response = f"{response}{user_message}{await responses.handle_response(user_message)}"
        if len(response) > 1900:
            # Split the response into smaller chunks of no more than 1900 characters each(Discord limit is 2000 per chunk)
            if "```" in response:
                # Split the response if the code block exists
                parts = response.split("```")
                # Send the first message
                await message.followup.send(parts[0])
                # Send the code block in a seperate message
                code_block = parts[1].split("\n")
                formatted_code_block = ""
                for line in code_block:
                    while len(line) > 1900:
                        # Split the line at the 50th character
                        formatted_code_block += line[:1900] + "\n"
                        line = line[1900:]
                    formatted_code_block += line + "\n"  # Add the line and seperate with new line

                # Send the code block in a separate message
                if (len(formatted_code_block) > 2000):
                    code_block_chunks = [formatted_code_block[i:i + 1900]
                                         for i in range(0, len(formatted_code_block), 1900)]
                    for chunk in code_block_chunks:
                        await message.followup.send("```" + chunk + "```")
                else:
                    await message.followup.send("```" + formatted_code_block + "```")

                # Send the remaining of the response in another message

                if len(parts) >= 3:
                    await message.followup.send(parts[2])
            else:
                response_chunks = [response[i:i + 1900]
                                   for i in range(0, len(response), 1900)]
                for chunk in response_chunks:
                    await message.followup.send(chunk)
        else:
            await message.followup.send(response)
    except Exception as e:
        await message.followup.send("> **Error: 出错了，请稍后重试!**")


async def send_start_prompt(client):
    import os.path

    config_dir = os.path.abspath(__file__ + "/../../")
    prompt_name = 'starting-prompt.txt'
    prompt_path = os.path.join(config_dir, prompt_name)
    try:
        if os.path.isfile(prompt_path) and os.path.getsize(prompt_path) > 0:
            with open(prompt_path, "r") as f:
                prompt = f.read()
                responseMessage = await responses.handle_response(prompt)
                if (config['discord_channel_id']):
                    channel = client.get_channel(int(config['discord_channel_id']))
                    await channel.send(responseMessage)
    except Exception as e:
        print(e)


class aclient(InitCog):
    @app_commands.command(name="chatgpt-chat", description="快来和ChatGPT聊天吧")
    async def chat(self, interaction: discord.Interaction, *, message: str):
        if interaction.user == self.client.user:
            return
        username = str(interaction.user)
        user_message = message
        channel = str(interaction.channel)
        await send_message(interaction, user_message)

    @app_commands.command(name="chatgpt-private", description="转为仅自己可见")
    async def private(self, interaction: discord.Interaction):
        global isPrivate
        await interaction.response.defer(ephemeral=False)
        if not isPrivate:
            isPrivate = not isPrivate
            await interaction.followup.send(
                "> **Info: 接下来的回复将只能由你自己可见，如果你想所有人看到chatGPT的回复，请使用`/public`指令**")
        else:
            await interaction.followup.send(
                "> **Warn: 你已经设置过仅自己可见，如果你想所有人看到chatGPT的回复，请使用`/public`指令**")

    @app_commands.command(name="chatgpt-public", description="转为所有人可见")
    async def public(self, interaction: discord.Interaction):
        global isPrivate
        await interaction.response.defer(ephemeral=False)
        if isPrivate:
            isPrivate = not isPrivate
            await interaction.followup.send(
                "> **Info: 接下来的回复将直接发送到聊天频道中，如果你只想自己看到chatGPT的回复，请使用`/private`指令**")
        else:
            await interaction.followup.send(
                "> **Warn: 你已经设置过所有人可见，如果你只想自己看到chatGPT的回复，请使用`/private`指令**")


async def setup(client):
    await client.add_cog(aclient(client))
