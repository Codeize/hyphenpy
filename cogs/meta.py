import discord
from discord.ext import commands

class Meta(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} has been loaded\n-----")

    @commands.command(name="Setup", aliases=["start"], description="Setup Hyphen in the server.")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx):
        embed = discord.Embed(title="Setup!", description="Configure Hyphen With This Server!", color=ctx.message.author.color)
        embed.add_field(name="**Firstly:**", value="Run -setuplogs and provide the ID of the desired channel!")
        await ctx.send(embed=embed)

    @commands.command(name="Set Logs", description="Set the logs channel for Hyphen.")
    async def setuplogs(self, ctx, *, logs=None):
        embed = discord.Embed(title="Logs Channel Set!", description=(f"The guild logs channel has been set to `<@#{logs}>`!"), colour=ctx.author.colour)
        await ctx.send(embed=embed)
        await self.client.setup.upsert({"_id": ctx.guild.id, "_logsid": logs})

def setup(client):
    client.add_cog(Meta(client))
