from discord.ext import commands

import statcord


class StatcordPost(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.key = "statcord.com-Q1EYrZnNBkjeLMWkERwf"
        self.api = statcord.Client(self.client,self.key)
        self.api.start_loop()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} has been loaded\n-----")


    @commands.Cog.listener()
    async def on_command(self,ctx):
        self.api.command_run(ctx)


def setup(client):
    client.add_cog(StatcordPost(client))