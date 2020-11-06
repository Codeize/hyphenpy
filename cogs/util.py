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

    @commands.command()
    async def updates(self, ctx):
        embed = discord.Embed(title="Hyphen Updates!", color=0x12e612)
        embed.add_field(name="Under Development :", value="Permission Checks, Logging, More Moderation Commands.")
        embed.add_field(name="Coming Soon :", value="Music, Economy.")

        embed.set_footer(text=f"Developed By Codeize#0001  | {self.client.user.name}")
        embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def stats(self, ctx):
        serverCount = len(self.client.guilds)
        memberCount = len(set(self.client.get_all_members()))

        embed = discord.Embed(title=f'{self.client.user.name} Stats', colour=ctx.author.colour, timestamp=ctx.message.created_at)

        embed.add_field(name='Bot Version:', value="0.0.1")
        embed.add_field(name='Total Guilds:', value=serverCount)
        embed.add_field(name='Total Users:', value=memberCount)
        embed.add_field(name='Bot Developers:', value="<@668423998777982997>")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Util(client))