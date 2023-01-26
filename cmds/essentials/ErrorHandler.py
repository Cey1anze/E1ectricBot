from discord.ext import commands

from Basic_bot.Core.init_cog import InitCog
from cmds.GuildManager.Member import Member


class Global_ErrorHandler(InitCog):

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        error_command = '{0}_error'.format(ctx.command)
        if hasattr(Custom_Handler, error_command):  # 檢查是否有 Custom Error Handler
            error_cmd = getattr(Custom_Handler, error_command)
            await error_cmd(self, ctx, error)
            return

        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send('缺少参数')
        elif isinstance(error, commands.errors.CommandNotFound):
            await ctx.send('指令不存在')
        elif isinstance(error, commands.errors.UserInputError):
            await ctx.send('参数输入有误')
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.send("**你无权做此操作！！！**")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'在{round(error.retry_after)} 秒后重试', delete_after=10)
        else:
            try:
                pass
            except Exception as e:
                await ctx.send(f'{e}')


class Custom_Handler:

    @Member.kickmember.error
    async def kick_error(self, error, ctx):
        if isinstance(error, commands.errors.MissingPermissions):
            await ctx.send("**你无权做此项操作！**")

    @Member.ban.error
    async def ban_error(self, error, ctx):
        if isinstance(error, commands.errors.MissingPermissions):
            await ctx.send("**你无权做此项操作！**")

    @Member.unban.error
    async def unban_error(self, error, ctx):
        if isinstance(error, commands.errors.MissingPermissions):
            await ctx.send("**你无权做此项操作！**")


async def setup(client):
    await client.add_cog(Global_ErrorHandler(client))
