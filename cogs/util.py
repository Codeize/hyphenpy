import discord
import time
from discord.ext import commands
import json

import cogs._json

class Util(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} has been loaded\n-----")

    @commands.command()
    async def ping(self, ctx):
        embed = discord.Embed(title="Pong!", description=(("You requested sir, : Pong! {0}ms").format(round(self.client.latency * 1000))), color=0x12e612)
        await ctx.send(embed=embed)

    @commands.command()
    async def updates(self, ctx):
        embed = discord.Embed(title="Hyphen Updates!", color=0x12e612)
        embed.add_field(name="Under Development :", value="Permission Checks, Logging, More Moderation Commands. Reason for shutdown cmd")
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
        embed.add_field(name="Thank You!", value=(f"Hey, **many, many** thanks to the {serverCount} servers and many more people who have halped Hyphen grow. Let's keep it going ||-invite||!"))
        await ctx.send(embed=embed)

    @commands.command()
    async def invite(self, ctx):
        embed = discord.Embed(title="Wanna get Hyphen in your server?", description="Here is the link to [add Hyphen](https://discord.com/api/oauth2/authorize?client_id=745622142657364040&permissions=8&scope=bot)!", colour=ctx.author.colour)
        await ctx.send(embed=embed)

    @commands.command()
    async def support(self, ctx):
        embed = discord.Embed(title="Need Support?", description="Here is the link to the [support server](https://discord.gg/TvMz7n7J)!", colour=ctx.author.colour)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def prefix(self, ctx, *, pre="-"):
        data = cogs._json.read_json("prefixes")
        data[str(ctx.message.guild.id)] = pre
        cogs._json.write_json(data, 'prefixes')
        embed = discord.Embed(title="Prefix Changed!", description=(f"The guild prefix has been set to `{pre}`. Use `{pre}prefix <prefix>` to change it again!"), colour=ctx.author.colour)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Util(client))