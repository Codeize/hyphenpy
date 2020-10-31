import discord
import time
from discord.ext import commands

class Util(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Utils is successfully loaded.")

    @commands.command()
    async def ping(self, ctx):
        embed = discord.Embed(title="Pong!", description=(("You requested sir, : Pong! {0}ms").format(round(self.client.latency * 1000))), color=0x12e612)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Util(client))