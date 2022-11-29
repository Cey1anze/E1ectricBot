import discord
import json
from discord.ext import commands
from Basic_bot.Core.init_cog import InitCog
from discord.utils import get


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
            await ctx.send(embed=discord.Embed(description=f'{arg} 已从 {oldrole} 移除，并加入到 {newrole}',
                                               colour=discord.Color.from_rgb(130, 156, 242)))
        else:  # dont remove other
            await arg.add_roles(newrole)
            await ctx.send(embed=discord.Embed(description=f'{arg} 已加入到 {newrole}',
                                               colour=discord.Color.from_rgb(130, 156, 242)))

    # kick member by command,example: ?kick @user
    @commands.command(name='kick', help='踢除用户')
    @commands.is_owner()
    async def kickmember(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.channel.purge(limit=1)
        await ctx.send(embed=discord.Embed(description=f'{member} 已被踢出，原因:{reason}',
                                           colour=discord.Color.from_rgb(130, 156, 242)))

    # ban member by command,example: ?ban @user
    @commands.command(name='ban', help='封禁用户')
    @commands.is_owner()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.channel.purge(limit=1)
        await ctx.send(embed=discord.Embed(description=f'{member} 已被封禁，原因:{reason}',
                                           colour=discord.Color.from_rgb(130, 156, 242)))

    # unban member by command,example: ?unban @user
    @commands.command(name='unban', help='解封用户')
    @commands.guild_only()
    @commands.is_owner()
    async def unban(self, ctx, userId):
        user = discord.Object(id=userId)
        await ctx.guild.unban(user)
        await ctx.channel.purge(limit=1)
        await ctx.send(embed=discord.Embed(description=f'已解除 {userId} 的封禁',
                                           colour=discord.Color.from_rgb(130, 156, 242)))


async def setup(client):
    await client.add_cog(Member(client))
