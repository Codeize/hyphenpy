import discord
from discord.ext import commands

class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} has been loaded\n-----")

    @commands.command()
    async def kick(self, ctx, member : discord.Member, *, reason="No reason was provided"):
        embed = discord.Embed(title="User Kicked!", description=(f"User : {member.mention}, was kicked by Staff member : {ctx.message.author.mention}. \n With the reason : {reason}!"), color=0x31e30e)
        await ctx.send(embed=embed)
        await member.kick(reason=reason)

        channel = self.client.get_channel(774727230122622976)

        embed1 = discord.Embed(title="User Kicked!", description=(f"User : {member.mention}, was kicked by Staff member : {ctx.message.author.mention}. \n With the reason : {reason}!"), color=0x31e30e)
        await channel.send(embed=embed1)

    @commands.command()
    async def ban(self, ctx, member : discord.Member, *, reason="No reason was provided"):
        server = ctx.message.guild
        embed = discord.Embed(title="User Banned!", description=(f"User : {member.mention}, was banned by Staff member : {ctx.message.author.mention}. \n With the reason : {reason}!"), color=0x31e30e)
        await ctx.send(embed=embed)
        await member.ban(reason=reason)

        channel = self.client.get_channel(774727230122622976)

        embed1 = discord.Embed(title="User Banned!", description=(f"User : {member.mention}, was banned by Staff member : {ctx.message.author.mention}. \n With the reason : {reason}!"), color=0x31e30e)
        await channel.send(embed=embed1)
        
        embed2 = discord.Embed(title=(f"You have been permanently banned from {server.name}!"), description=(f"Well, this is awkward...\nYou were banned by Staff member : {ctx.message.author} with the reason : {reason}!"), color=0x31e30e)
        try:
            await member.send(embed=embed2)
            print(f"Messages succeded in sending to {member.name}")
        
        except discord.Forbidden:
            print("User has DMs disabled.")

    @commands.command()
    async def unban(self, ctx, *, member):
        bannedUsers = await ctx.guild.bans()
        memberName, memberDiscriminator = member.split("#")

        for banEntry in bannedUsers:
            user = banEntry.user

            if (user.name, user.discriminator) == (user.name, user.discriminator):
                embed = discord.Embed(title="User Unbanned!", description=(f"User : {member}, was unbanned by Staff member : {ctx.message.author.mention}!"), color=0x31e30e)
                await ctx.send(embed=embed)
                await ctx.guild.unban(user)

        channel = self.client.get_channel(774727230122622976)

        embed1 = discord.Embed(title="User Unbanned!", description=(f"User : {member}, was unbanned by Staff member : {ctx.message.author.mention}!"), color=0x31e30e)
        await channel.send(embed=embed1)

    @commands.command()
    async def clear(self, ctx, amount : int):
        await ctx.channel.purge(limit=amount+1)
        embed = discord.Embed(title="Purged Message(s)!",  description=(f"Purged {amount} message(s)!"), color=0x31e30e)
        await ctx.send(embed=embed)
        await ctx.message.delete()
        
        embed1 = discord.Embed(title="Purged Message(s)!",  description=(f"Purged {amount} message(s) in channel <#{ctx.message.channel.id}>!"), color=0x31e30e)
        await ctx.send(embed=embed1)

def setup(client):
    client.add_cog(Moderation(client))