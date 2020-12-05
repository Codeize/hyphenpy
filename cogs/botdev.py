import discord
from discord.ext import commands
import json

class Botdev(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"\n__COGS__\n{self.__class__.__name__} has been loaded\n-----")

    @commands.command(name="Shutdown", description="(Bot Developer Only!) Terminates Hyphens current session.")
    @commands.is_owner()
    async def shutdown(self, ctx):
        embed = discord.Embed(title="Logged Out!", description="Ok. Process successfully voided. - (Code 0)", color=0x12e612)
        await ctx.send(embed=embed)
        await self.client.logout()

#@commands.command(name="Blacklist", description="(Bot Developer Only!) Blacklists the specified user.")
#@commands.is_owner()
#async def blacklist(self, ctx, user: discord.Member, *, reason="No reason was provided"):
##if ctx.message.author.id == user.id:
###await ctx.send("Really? You cannot blacklist yourself stoopid!")
###return

##self.client.blacklisted_users.append(user.id)
##data = cogs._json.read_json("blacklist")
##data["blacklistedUsers"].append(user.id)
##cogs._json.write_json(data, "blacklist")
##embed = discord.Embed(title="User Blacklisted!", description=(f"User : {user.mention}, was blacklisted by Codeize. \n With the reason : {reason}!"), color=0x31e30e)
##await ctx.send(embed=embed)

    #@commands.command(name="Unblacklist", description="(Bot Developer Only!) Unblacklists the specified blacklisted user.")
    #@commands.is_owner()
    #async def unblacklist(self, ctx, user: discord.Member, *, reason="No reason was provided"):
        #self.client.blacklisted_users.remove(user.id)
        #data = cogs._json.read_json("blacklist")
        #data["blacklistedUsers"].remove(user.id)
        #cogs._json.write_json(data, "blacklist")
        #embed = discord.Embed(title="User Unblacklisted!", description=(f"User : {user.mention}, was unblacklisted by Codeize. \n With the reason : {reason}!"), color=0x31e30e)
        #await ctx.send(embed=embed)

    #@commands.command()
    #@commands.is_owner()
    #async def dev(self, ctx):
        #embed = discord.Embed(title="Entered Dev Mode!", description=(f"Port : **8080** Version : **0.0.3**."), color=0x31e30e)
        #await ctx.send(embed=embed)#
        #await ctx.send("THIS IS A DEVELOPMENT BUILD OF HYPHEN!\nALL FEATURES MAY NOT PERFORM AS INTENDED!")

def setup(client):
    client.add_cog(Botdev(client))