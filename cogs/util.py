import discord
import time
from discord.ext import commands
import json
import datetime

start_time = time.time()

class Util(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} has been loaded\n-----")

    @commands.command(name="Ping", description="Shows Watchdog's current latency.")
    async def ping(self, ctx):
        embed = discord.Embed(title="Pong!", description=(("You requested sir, : Pong! {0}ms").format(round(self.client.latency * 1000))), color=0x12e612)
        await ctx.send(embed=embed)

    @commands.command(name="stats", description="Shows stats about Watchdog")
    async def stats(self, ctx):
        serverCount = len(self.client.guilds)
        memberCount = len(set(self.client.get_all_members()))
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))

        embed = discord.Embed(title=f'{self.client.user.name} Stats', colour=ctx.author.colour, timestamp=ctx.message.created_at)

        embed.add_field(name='Bot Version:', value="0.0.2")
        embed.add_field(name='dpy:', value=(f"{discord.version_info}."))
        embed.add_field(name='Total Guilds:', value=serverCount)
        embed.add_field(name='Total Users:', value=memberCount)
        embed.add_field(name='Uptime:', value=text)
        embed.add_field(name='Bot Developers:', value="<@668423998777982997>")
        embed.add_field(name="Thank You!", value=(f"Hey, **many, many** thanks to the {serverCount} servers and many more people who have helped Watchdog grow. Let's keep it going ||-invite||!"))
        await ctx.send(embed=embed)

    @commands.command(name="Uptime", description="Shows Watchdogs current uptime.")
    async def uptime(self, ctx):
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))
        embed = discord.Embed(title="Uptime", description="I prefer uptime, not downtime! :)", colour=ctx.message.author.color)
        embed.add_field(name="Time Elapsed:", value=text)
        try:
            await ctx.send(embed=embed)
        except discord.HTTPException:
            await ctx.send("Current uptime: " + text)

    @commands.command(name="Invite", description="Invite Watchdog to your servers!")
    async def invite(self, ctx):
        embed = discord.Embed(title="Wanna get Watchdog in your server?", description="Here is the link to [add Watchdog](https://discord.com/api/oauth2/authorize?client_id=812031878881345607&permissions=8&scope=bot)!", colour=ctx.author.colour)
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

    @commands.command(name="credits", description="Many thanks to these users!")
    async def credits(self, ctx):
        embed = discord.Embed(title="The Credits!", description="**Huge** thanks to these users, Watchdog wouldn't have these features without your help!", colour=ctx.author.colour)
        embed.add_field(name="Its not an Apple#6103", value="Thanks for helping with the sharding process, when I need to add it that is!")
        embed.add_field(name="3vil#0001", value="Thanks for all the advice when I was getting started, and even now!")
        embed.add_field(name="Cookie_#7907", value="Thanks for a lot of development help, but mainly testing and feedback!")
        embed.add_field(name="Goose_#2548", value="Thanks for helping with technical issues!")
        embed.add_field(name="Extinct#1607", value="Thanks for all the support and enthusiasm during the early versions of Watchdog!")
        embed.add_field(name="Reiterpallasch#2732", value="Thanks for testing the early versions of Watchdog!")
        embed.add_field(name="Trung#3765", value="Thanks for giving feedback and promoting Watchdog!")
        embed.add_field(name="Skelmis#9135", value="Thanks for all the support, tips, and advice for Watchdog! But, most importantly, thanks for helping with the AntiSpam module!")
        embed.add_field(name="justjude#2296", value="Thanks for fixing some commands, and giving some great advice")
        await ctx.send(embed=embed)

    @commands.command(name="privacy", description="Shows Watchdogs Legal Policy.")
    async def privacy(self, ctx):
        embed = discord.Embed(title="The Boring Legal Stuff!", description="[Here](https://Watchdog.codeize.dev/privacy/) is my Privacy Policy!", colour=ctx.author.colour)
        await ctx.send(embed=embed)
    
    @commands.command(name="Channel Stats", aliases=['cs'], description="Sends a nice fancy embed with some channel stats!")
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def channelstats(self, ctx):
        """
        Sends a nice fancy embed with some channel stats
        """
        channel = ctx.channel
        embed = discord.Embed(title=f"Stats for **{channel.name}**", description=f"{'Category: {}'.format(channel.category.name) if channel.category else 'This channel is not in a category'}", color=ctx.author.color)
        embed.add_field(name="Channel Guild", value=ctx.guild.name, inline=False)
        embed.add_field(name="Channel Id", value=channel.id, inline=False)
        embed.add_field(name="Channel Description", value=f"{channel.topic if channel.topic else 'No description!.'}", inline=False)
        embed.add_field(name="Channel Position", value=channel.position, inline=False)
        embed.add_field(name="Channel Slowmode Delay", value=channel.slowmode_delay, inline=False)
        embed.add_field(name="Channel is marked as NSFW", value=channel.is_nsfw(), inline=False)
        embed.add_field(name="Channel is a News channel", value=channel.is_news(), inline=False)
        embed.add_field(name="Channel Creation Time", value=channel.created_at, inline=False)
        embed.add_field(name="Channel Permissions Synced", value=channel.permissions_synced, inline=False)

        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Util(client))