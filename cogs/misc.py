import discord
from discord.ext import commands

class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Misc is successfully loaded.")

    @commands.command()
    async def echo(self, ctx, *, message=None):
        message = message or "Please provide the message to be echoed!"
        await ctx.message.delete()
        await ctx.send(message)


def setup(client):
    client.add_cog(Misc(client))