from discord.utils import get
from discord.ext import commands
from Basic_bot.Core.init_cog import InitCog
from Basic_bot.Core import loadjson

jdata = loadjson.load_mainconfig()


class ChannelManage(InitCog):

    # Response when a new member join
    @commands.Cog.listener()
    async def on_member_join(self, member):
        welchannel = self.client.get_channel(int(jdata['welchannel-id']))
        # Optional : give a role when new members join,id = role_id,Separate roles from online status
        role = get(member.guild.roles, id=1046023381612511302)
        await welchannel.send(f'欢迎 {member} 进入频道')
        # give a role when new member joined,id = role_id
        await member.add_roles(role)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        levchannel = self.client.get_channel(int(jdata['welchannel-id']))
        await levchannel.send(f'{member} 退出了频道')


async def setup(client):
    await client.add_cog(ChannelManage(client))
