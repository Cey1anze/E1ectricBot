from discord.ext import commands
from Core.init_cog import InitCog
from Core import loadjson, logger

channel = loadjson.load_channelconfig()
logs = loadjson.load_logconfig()


class ChannelManage(InitCog):

    # Response when a new member join
    @commands.Cog.listener()
    async def on_member_join(self, member):
        welchannel = self.client.get_channel(int(channel['welchannel-id']))
        await welchannel.send(f'欢迎 {member} 进入频道')
        logger.logwrite(
            f'{member} 加入了频道'
        )
        await logger.dclogwrite(
            channel=self.client.get_channel(logs['logger_channel']),
            msg=f'{member} 加入了频道'
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        welchannel = self.client.get_channel(int(channel['welchannel-id']))
        await welchannel.send(f'{member} 退出了频道')
        logger.logwrite(
            f'{member} 退出了频道'
        )
        await logger.dclogwrite(
            channel=self.client.get_channel(logs['logger_channel']),
            msg=f'{member} 退出了频道'
        )


async def setup(client):
    await client.add_cog(ChannelManage(client))
