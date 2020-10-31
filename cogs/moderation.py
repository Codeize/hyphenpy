import discord
from discord.ext import commands

class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Moderation is successfully loaded.")

    @client.command()
    async def kick(self, ctx, member : discord.Member, *, reason="No reason was provided"):
        embed = discord.Embed(title="User Kicked!", description=(f"User : {member.mention}, was kicked by Staff member : {ctx.message.author.mention}. \n With the reason : {reason}!"), color=0x31e30e)
        await ctx.send(embed=embed)
        await member.kick(reason=reason)

    @client.command()
    async def ban(self, ctx, member : discord.Member, *, reason="No reason was provided"):
        embed = discord.Embed(title="User Banned!", description=(f"User : {member.mention}, was banned by Staff member : {ctx.message.author.mention}. \n With the reason : {reason}!"), color=0x31e30e)
        await ctx.send(embed=embed)
        await member.ban(reason=reason)

    @client.command()
    async def unban(self, ctx, *, member):
        bannedUsers = await ctx.guild.bans()
        memberName, memberDiscriminator = member.split("#")

        for banEntry in bannedUsers:
            user = banEntry.user

            if (user.name, user.discriminator) == (user.name, user.discriminator):
                embed = discord.Embed(title="User Unbanned!", description=(f"User : {member}, was unbanned by Staff member : {ctx.message.author.mention}!"), color=0x31e30e)
                await ctx.send(embed=embed)
                await ctx.guild.unban(user)

    @client.command()
    async def clear(self, ctx, amount : int):
        await ctx.channel.purge(limit=amount)
        embed = discord.Embed(title="Purged Message(s)!",  description=(f"Purged {amount} message(s)!"), color=0x31e30e)
        await ctx.send(embed=embed)
        await ctx.message.delete()

def setup(client):
    client.add_cog(Moderation(client))