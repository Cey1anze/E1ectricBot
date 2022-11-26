import discord
import json
from discord.ext import commands
from Basic_bot.Core.init_cog import InitCog
from discord.utils import get


class Member(InitCog):

    # give someone a role by commands,example: ?add-role @user [true/false] [new-role's name] [old-role's name]
    # this example means user joined test1 and removed from test : ?add-role @user true test1 test
    # old-role can be multiple
    # true:remove from old-role and join new-role,false:join new-role directly
    @commands.command(name='add-role', help='give member a role')
    async def addrole(self, ctx, arg: discord.Member, arg1: bool, arg2: str, *, arg3: str):
        oldrole = get(ctx.guild.roles, name=arg3)
        newrole = get(ctx.guild.roles, name=arg2)
        if arg1:  # remove from old-role and join new-role
            await arg.remove_roles(oldrole)
            await arg.add_roles(newrole)
            await ctx.send(f'{arg} already removed from {oldrole} and joined {newrole}')
        else:  # dont remove other
            await arg.add_roles(newrole)
            await ctx.send(f'{arg} already joined {newrole}')

    # kick member by command,example: ?kick @user
    @commands.command(name='kick', help='kick member from guild')
    async def kickmember(self, ctx, member: discord.Member, *, reason: str):
        await member.kick(reason=reason)
        await ctx.send(f'{member} kicked,reason:{reason}')

    # ban member by command,example: ?ban @user
    @commands.command(name='ban', help='ban member from guild')
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'{member} banned,reason:{reason}')

    # unban member by command,example: ?unban @user
    @commands.command(name='unban', help='ban member from guild')
    @commands.guild_only()
    async def unban(self, ctx, userId):
        user = discord.Object(id=userId)
        await ctx.guild.unban(user)
        await ctx.send(f"Unbanned {userId}")


async def setup(client):
    await client.add_cog(Member(client))
