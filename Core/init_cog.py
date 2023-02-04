from discord.ext import commands


class InitCog(commands.Cog):
    def __init__(self, client):
        self.client = client
