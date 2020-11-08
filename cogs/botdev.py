import discord
from discord.ext import commands
import json

import cogs._json

class Botdev(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"\n__COGS__\n{self.__class__.__name__} has been loaded\n-----")

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        embed = discord.Embed(title="Logged Out!", description="Ok. Process successfully voided. - (Code 0)", color=0x12e612)
        await ctx.send(embed=embed)
        await self.client.logout()

    @commands.command()
    @commands.is_owner()
    async def blacklist(self, ctx, user: discord.Member, *, reason="No reason was provided"):
        if ctx.message.author.id == user.id:
            await ctx.send("Really? You cannot blacklist yourself stoopid!")
            return

        self.client.blacklisted_users.append(user.id)
        data = cogs._json.read_json("blacklist")
        data["blacklistedUsers"].append(user.id)
        cogs._json.write_json(data, "blacklist")
        embed = discord.Embed(title="User Blacklisted!", description=(f"User : {user.mention}, was blacklisted by Codeize. \n With the reason : {reason}!"), color=0x31e30e)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def unblacklist(self, ctx, user: discord.Member, *, reason="No reason was provided"):
        self.client.blacklisted_users.remove(user.id)
        data = cogs._json.read_json("blacklist")
        data["blacklistedUsers"].remove(user.id)
        cogs._json.write_json(data, "blacklist")
        embed = discord.Embed(title="User Unblacklisted!", description=(f"User : {user.mention}, was unblacklisted by Codeize. \n With the reason : {reason}!"), color=0x31e30e)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def fv(self, ctx):
        channel = self.client.get_channel(764518143108317194)
        
        embed = discord.Embed(title="Verify Below!", description="Hey! Welcome to the server! For verification, security and raid prevention purposes, we have a *tiny*, *tiny*  little verification system in place, all you gotta do is react to this message to gain access to the rest of the server. (Easy, Right?). Make sure to read the <#764489837851050014>.If you're having problems please DM one of the <@&764516812225904641>.\nEnjoy your stay :)", color=0x42cef5)
        await channel.send(embed=embed)

def setup(client):
    client.add_cog(Botdev(client))