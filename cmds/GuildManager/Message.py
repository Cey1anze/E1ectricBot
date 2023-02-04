import discord
from discord import app_commands
from discord.ext import commands

from Core import logger, loadjson
from Core.init_cog import InitCog

logs = loadjson.load_logconfig()

is_cleaning = False


class Message(InitCog):

    @app_commands.command(name='clean', description='清除消息')
    @app_commands.describe(num='要清理多少条消息')
    @commands.has_permissions(manage_channels=True)
    async def clean(self, interaction: discord.Interaction, num: int):
        global is_cleaning
        is_cleaning = True
        await interaction.channel.purge(limit=num)
        is_cleaning = False
        await interaction.response.defer()
        await interaction.followup.send(
            embed=discord.Embed(description=f'已删除 **{num}** 条消息',
                                colour=discord.Color.from_rgb(130, 156, 242))
        )

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not is_cleaning:
            if not message.author.bot:
                logger.logwrite(
                    f'{message.author} 在频道：{message.channel} 删除了一条消息: {message.content}'
                )
                await logger.dclogwrite(
                    channel=self.client.get_channel(logs['logger_channel']),
                    msg=f'{message.author} 在频道：{message.channel} 删除了一条消息: {message.content}'
                )


async def setup(client):
    await client.add_cog(Message(client))
