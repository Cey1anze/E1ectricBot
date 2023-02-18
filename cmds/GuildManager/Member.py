import datetime

import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
from discord.utils import get

from Core import logger, loadjson
from Core.init_cog import InitCog

logs = loadjson.load_logconfig()
reaction = loadjson.load_reactionconfig()
current_role = []


class Member(InitCog):

    # give someone a role by commands,example: ?add-role @user [true/false] [old-role's name] [new-role's name]
    # this example means user joined test and removed from test1 : ?add-role @user true test1 test
    # old-role can be multiple
    # true:remove from old-role and join new-role,false:join new-role directly
    @commands.command(name='add-role', help='给予身份组')
    @commands.is_owner()
    async def addrole(self, ctx, arg: discord.Member, arg1: bool, arg2: str, *, arg3: str):
        oldrole = get(ctx.guild.roles, name=arg2)
        newrole = get(ctx.guild.roles, name=arg3)
        await ctx.channel.purge(limit=1)
        if arg1:  # remove from old-role and join new-role
            await arg.remove_roles(oldrole)
            await arg.add_roles(newrole)
            await ctx.send(
                embed=discord.Embed(description=f'{arg} 已从 {oldrole} 移除，并加入到 {newrole}',
                                    colour=discord.Color.from_rgb(130, 156, 242))
            )
        else:  # dont remove other
            await arg.add_roles(newrole)
            await ctx.send(
                embed=discord.Embed(description=f'{arg} 已加入到 {newrole}',
                                    colour=discord.Color.from_rgb(130, 156, 242))
            )

    # kick member by command,example: ?kick @user
    @commands.command(name='kick', help='踢除用户')
    @commands.has_permissions(kick_members=True)
    async def kickmember(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.channel.purge(limit=1)
        await ctx.send(
            embed=discord.Embed(description=f'{member} 已被踢出，原因:{reason}',
                                colour=discord.Color.from_rgb(130, 156, 242))
        )
        logger.logwrite(
            f'{ctx.author} 已踢出 {member} , 原因 : {reason}'
        )
        await logger.dclogwrite(
            channel=self.client.get_channel(logs['logger_channel']),
            msg=f'{ctx.author} 已踢出 {member} , 原因 : {reason}'
        )

    # ban member by command,example: ?ban @user
    @commands.command(name='ban', help='封禁用户')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.channel.purge(limit=1)
        await ctx.send(
            embed=discord.Embed(description=f'{member} 已被封禁，原因:{reason}',
                                colour=discord.Color.from_rgb(130, 156, 242))
        )
        logger.logwrite(
            f'{ctx.author} 已封禁 {member} , 原因 : {reason}'
        )
        await logger.dclogwrite(
            channel=self.client.get_channel(logs['logger_channel']),
            msg=f'{ctx.author} 已封禁 {member} , 原因 : {reason}'
        )

    @app_commands.command(name='mute', description='静音用户')
    @app_commands.describe(reason='静音的原因')
    async def mute(self, interaction: discord.Interaction, member: discord.Member, *, reason: str = None):
        if interaction.user.guild_permissions.mute_members:
            voice_state = member.voice
            if voice_state:
                await interaction.response.defer()
                await member.edit(mute=True, reason=reason)
                await interaction.followup.send(
                    embed=discord.Embed(description=f'{member} 已被静音 , 原因 : {reason}',
                                        colour=discord.Color.from_rgb(130, 156, 242))
                )
                logger.logwrite(
                    f'{member} 已被静音 , 原因 : {reason}'
                )
                await logger.dclogwrite(
                    channel=self.client.get_channel(logs['logger_channel']),
                    msg=f'{member} 已被静音 , 原因 : {reason}'
                )
            else:
                await interaction.response.defer()
                await interaction.followup.send(
                    embed=discord.Embed(description=f'**{member}** 不在任何语音频道中',
                                        colour=discord.Color.from_rgb(130, 156, 242))
                )

        else:
            await interaction.response.defer()
            await interaction.followup.send(
                embed=discord.Embed(description=f'{interaction.user.mention} 没有执行这项操作的权限',
                                    colour=discord.Color.from_rgb(130, 156, 242))
            )

    @app_commands.command(name='timeout', description='禁言用户')
    @app_commands.rename(option='禁言时间')
    @app_commands.describe(reason='禁言的原因')
    @app_commands.choices(option=[
        Choice(name='60秒', value=0),
        Choice(name='5分钟', value=1),
        Choice(name='10分钟', value=2),
        Choice(name='1小时', value=3),
        Choice(name='1天', value=4),
        Choice(name='1周', value=5)
    ])
    async def timeout(self, interaction: discord.Interaction, member: discord.Member, option: int, *,
                      reason: str = None):
        if not interaction.user.guild_permissions.moderate_members:
            await interaction.response.defer()
            await interaction.followup.send(
                embed=discord.Embed(description=f'{interaction.user.mention} 没有执行这项操作的权限',
                                    colour=discord.Color.from_rgb(130, 156, 242))
            )
            return

        duration_map = {
            0: datetime.timedelta(minutes=1.0),
            1: datetime.timedelta(minutes=5.0),
            2: datetime.timedelta(minutes=10.0),
            3: datetime.timedelta(hours=1.0),
            4: datetime.timedelta(days=1.0),
            5: datetime.timedelta(weeks=1.0),
        }

        duration = duration_map.get(option, datetime.timedelta(minutes=1.0))
        await interaction.response.defer()
        await member.timeout(duration, reason=reason)
        await interaction.followup.send(
            embed=discord.Embed(description=f'{member} 已被禁言 **{duration}**, 原因 : {reason}',
                                colour=discord.Color.from_rgb(130, 156, 242))
        )
        logger.logwrite(
            f'{member} 已被禁言 **{duration}**, 原因 : {reason}'
        )
        await logger.dclogwrite(
            channel=self.client.get_channel(logs['logger_channel']),
            msg=f'{member} 已被禁言 **{duration}**, 原因 : {reason}'
        )

    # unban member by command,example: ?unban @user
    @commands.command(name='unban', help='解封用户')
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def unban(self, ctx, userId):
        user = discord.Object(id=userId)
        await ctx.guild.unban(user)
        await ctx.channel.purge(limit=1)
        await ctx.send(
            embed=discord.Embed(description=f'已解除 {userId} 的封禁',
                                colour=discord.Color.from_rgb(130, 156, 242))
        )
        logger.logwrite(
            f'{ctx.author} 已解除 {userId} 的封禁'
        )
        await logger.dclogwrite(
            channel=self.client.get_channel(logs['logger_channel']),
            msg=f'{ctx.author} 已解除 {userId} 的封禁'
        )

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # 检查贴纸是否是您所期望的贴纸
        if payload.message_id == reaction['Message_id']:
            # 从消息所在的服务器中获取成员
            guild = self.client.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            if member is not None:
                # 将成员添加到身份组中
                emoji = payload.emoji
                role = None
                if emoji == reaction['emoji'][0]:
                    role = discord.utils.get(guild.roles, name=reaction['role_name'][0])
                elif emoji.name == reaction['emoji'][1]:
                    role = discord.utils.get(guild.roles, name=reaction['role_name'][1])
                elif emoji.name == reaction['emoji'][2]:
                    role = discord.utils.get(guild.roles, name=reaction['role_name'][2])
                elif emoji.name == reaction['emoji'][3]:
                    role = discord.utils.get(guild.roles, name=reaction['role_name'][3])

                if role is not None:
                    await member.add_roles(role)
                    current_role.append(role)
                if len(current_role) > 1:
                    index = current_role.index(role)
                    await member.remove_roles(current_role.pop(index - 1))

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        # 检查贴纸是否是您所期望的贴纸
        if payload.message_id == reaction['Message_id']:
            # 从消息所在的服务器中获取成员
            guild = self.client.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            if member is not None:
                role = None
                # 将成员添加到身份组中
                emoji = payload.emoji
                if emoji == reaction['emoji'][0]:
                    role = discord.utils.get(guild.roles, name=reaction['role_name'][0])
                elif emoji.name == reaction['emoji'][1]:
                    role = discord.utils.get(guild.roles, name=reaction['role_name'][1])
                elif emoji.name == reaction['emoji'][2]:
                    role = discord.utils.get(guild.roles, name=reaction['role_name'][2])
                elif emoji.name == reaction['emoji'][3]:
                    role = discord.utils.get(guild.roles, name=reaction['role_name'][3])
                if role is not None and role in member.roles:
                    await member.remove_roles(role)
                    current_role.remove(role)


async def setup(client):
    await client.add_cog(Member(client))
