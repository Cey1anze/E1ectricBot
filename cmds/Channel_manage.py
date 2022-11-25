from discord.ext import commands
from Basic_bot.Core.init_cog import InitCog
from Basic_bot.Core import loadjson

jdata = loadjson.load_mainconfig()


class ChannelManage(InitCog):

    @commands.Cog.listener()
    async def on_member_join(self, member):
        welchannel = self.client.get_channel(int(jdata['welchannel-id']))
        await welchannel.send(f'欢迎 {member} 进入频道')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        levchannel = self.client.get_channel(int(jdata['welchannel-id']))
        await levchannel.send(f'{member} 退出了频道')


async def setup(client):
    await client.add_cog(ChannelManage(client))
