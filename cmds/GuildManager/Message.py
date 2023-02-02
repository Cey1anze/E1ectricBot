import discord
from discord import app_commands
from discord.ext import commands

from Core.init_cog import InitCog
from Core import logger, loadjson

logs = loadjson.load_logconfig()


class Message(InitCog):

    # clean messages
    @app_commands.command(name='clean', description='清除消息')
    @app_commands.describe(num='要清理多少条消息')
    @commands.has_permissions(manage_channels=True)
    async def clean(self, interaction: discord.Interaction, num: int):
        try:
            await interaction.channel.purge(limit=num)
            await interaction.response.defer()
            await interaction.followup.send(embed=discord.Embed(description=f'已删除 **{num}** 条消息',
                                                                colour=discord.Color.from_rgb(130, 156, 242)))
        except Exception as e:
            print(e)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        logger.logwrite(f'{message.author} 在 {message.channel} 删除了一条消息: {message.content}')
        await logger.dclogwrite(channel=self.client.get_channel(logs['logger_channel']),
                                msg=f'{message.author} 在 {message.channel} 删除了一条消息: {message.content}')


async def setup(client):
    await client.add_cog(Message(client))
