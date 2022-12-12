import asyncio
import discord
import json
from discord import app_commands
from discord.ext import commands
from Basic_bot.Core.init_cog import InitCog


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


async def setup(client):
    await client.add_cog(Message(client))
