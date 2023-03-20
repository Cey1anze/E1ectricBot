import discord
from Core.init_cog import InitCog


def user_not_joined() -> discord.Embed:
    return discord.Embed(title='请先加入语音频道', colour=discord.Color.red())


def bot_not_joined() -> discord.Embed:
    return discord.Embed(title='机器人未进入语音频道', colour=discord.Color.red())


def joined_voice() -> discord.Embed:
    return discord.Embed(title='机器人已加入语音频道', colour=discord.Color.green())


def leaved_voice() -> discord.Embed:
    return discord.Embed(title='机器人已离开语音频道', colour=discord.Color.green())


def music_not_playing() -> discord.Embed:
    return discord.Embed(title='请先播放音乐', colour=discord.Color.red())


def vol_input_error() -> discord.Embed:
    return discord.Embed(title='请输入正确的音量', colour=discord.Color.red())


def vol_setted(volume) -> discord.Embed:
    return discord.Embed(title='已设置音量为{}%'.format(volume * 100), colour=discord.Color.green())


def music_paused() -> discord.Embed:
    return discord.Embed(title='已暂停播放', colour=discord.Color.green())


def music_not_paused() -> discord.Embed:
    return discord.Embed(title='音乐未被暂停', colour=discord.Color.red())


def music_resumed() -> discord.Embed:
    return discord.Embed(title='已继续播放', colour=discord.Color.green())


def music_stoped() -> discord.Embed:
    return discord.Embed(title='已停止播放', colour=discord.Color.green())


def track_info(song_name, author, album_name, publish_time, album_pic_url) -> discord.Embed:
    track_embed = discord.Embed(title='歌曲信息', colour=discord.Colour.green())
    track_embed.add_field(name='歌名', value=song_name, inline=False)
    track_embed.add_field(name='歌手', value=author, inline=False)
    track_embed.add_field(name='专辑', value=album_name, inline=False)
    track_embed.add_field(name='发行时间',
                          value=publish_time,
                          inline=False)
    track_embed.set_thumbnail(url=album_pic_url)
    return track_embed


class Response(InitCog):
    pass


async def setup(client):
    await client.add_cog(Response(client))
