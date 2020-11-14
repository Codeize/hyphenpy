import discord
import time
from discord.ext import commands
import json

class Util(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} has been loaded\n-----")

    @commands.command(name="Ping", description="Shows Hyphen's current latency.")
    async def ping(self, ctx):
        embed = discord.Embed(title="Pong!", description=(("You requested sir, : Pong! {0}ms").format(round(self.client.latency * 1000))), color=0x12e612)
        await ctx.send(embed=embed)

    @commands.command(name="Updates", description="Keep up to date with Hyphen.")
    async def updates(self, ctx):
        embed = discord.Embed(title="Hyphen Updates!", color=0x12e612)
        embed.add_field(name="Under Development :", value="Permission Checks, Setup, More Moderation Commands. Reason for shutdown cmd")
        embed.add_field(name="Coming Soon :", value="Music, Economy.")

        embed.set_footer(text=f"Developed By Codeize#0001  | {self.client.user.name}")
        embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="stats", description="Shows stats about Hyphen")
    async def stats(self, ctx):
        serverCount = len(self.client.guilds)
        memberCount = len(set(self.client.get_all_members()))

        embed = discord.Embed(title=f'{self.client.user.name} Stats', colour=ctx.author.colour, timestamp=ctx.message.created_at)

        embed.add_field(name='Bot Version:', value="0.0.2")
        embed.add_field(name='dpy:', value=(f"{discord.version_info}."))
        embed.add_field(name='Total Guilds:', value=serverCount)
        embed.add_field(name='Total Users:', value=memberCount)
        embed.add_field(name='Bot Developers:', value="<@668423998777982997>")
        embed.add_field(name="Thank You!", value=(f"Hey, **many, many** thanks to the {serverCount} servers and many more people who have halped Hyphen grow. Let's keep it going ||-invite||!"))
        await ctx.send(embed=embed)

    @commands.command(name="Invite", description="Invite Hyphen to your servers!")
    async def invite(self, ctx):
        embed = discord.Embed(title="Wanna get Hyphen in your server?", description="Here is the link to [add Hyphen](https://discord.com/api/oauth2/authorize?client_id=745622142657364040&permissions=8&scope=bot)!", colour=ctx.author.colour)
        await ctx.send(embed=embed)

    @commands.command(name="Support", description="Invite to the support server.")
    async def support(self, ctx):
        embed = discord.Embed(title="Need Support?", description="Here is the link to the [support server](https://discord.gg/5fwPD4QxjJ)!", colour=ctx.author.colour)
        await ctx.send(embed=embed)

    @commands.command(name="prefix",aliases=["changeprefix", "setprefix", "cp"],description="Change your guilds prefix!",usage="[prefix]")
    @commands.has_guild_permissions(manage_guild=True)
    async def prefix(self, ctx, *, prefix="-"):
        await self.client.config.upsert({"_id": ctx.guild.id, "prefix": prefix})
        embed = discord.Embed(title="Prefix Changed!", description=(f"The guild prefix has been set to `{prefix}`. Use `{prefix}prefix [prefix]` to change it again!"), colour=ctx.author.colour)
        await ctx.send(embed=embed)

    @commands.command(name="deleteprefix", aliases=["dp"], description="Delete your guilds prefix!")
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    async def deleteprefix(self, ctx):
        await self.client.config.unset({"_id": ctx.guild.id, "prefix": 1})
        embed = discord.Embed(title="Prefix Erased!", description="This guilds prefix has been set back to the default! The default prefix is `-`", colour=ctx.author.colour)
        await ctx.send(embed=embed)

    @commands.command(name="credits", description="Many thanks to these users!")
    async def credits(self, ctx):
        embed = discord.Embed(title="The Credits!", description="**Huge** thanks to these users, Hyphen wouldn't have these features without your help!", colour=ctx.author.colour)
        embed.add_field(name="Its not an Apple#6103", value="Thanks for helping with the sharding process!")
        embed.add_field(name="3vil#0001", value="Thanks for all the advice when I was getting started, and even now!")
        embed.add_field(name="Cookie_#7907", value="Thanks for a lot of development help, but mainly testing and feedback!")
        embed.add_field(name="Goose_#2548", value="Thanks for helping with technical issues!")
        embed.add_field(name="Extinct#1607", value="Thanks for all the support and enthusiasm during the early versions of Hyphen!")
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Util(client))