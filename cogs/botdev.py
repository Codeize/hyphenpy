import discord
from discord.ext import commands
import json

class Botdev(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Botdev is successfully loaded.")

    data = read_json("blacklist")
    client.blacklistedUsers = data["blacklistedUsers"]

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        embed = discord.Embed(title="Logged Out!", description="Ok. Process successfully voided.", color=0x12e612)
        await ctx.send(embed=embed)
        await ctx.bot.logout()

    @commands.command()
    @commands.is_owner()
    async def blacklist(self, ctx, user: discord.Member, reason="No reason was provided"):
        if ctx.message.author.id == user.id:
            await ctx.send("Hey, you cannot blacklist yourself!")
            return

            self.client.blacklistedUsers.append(user.id)
            data = read_json("blacklist")
            data["blacklistedUsers"].append(user.id)
            write_json(data, "blacklist")
            embed = discord.Embed(title="User Blacklisted!", description=(f"{user} was blacklisted from using Hyphen by {ctx.author.mention}, \n with the reason : {reason}!"), color=0x12e612)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def unblacklist(self, ctx, user: discord.Member, reason="No reason was provided"):
        self.client.blacklistedUsers.remove(user.id)
        data = read_json("blacklist")
        data["blacklistedUsers"].remove(user.id)
        write_json(data, "blacklist")
        embed = discord.Embed(title="User Unblacklisted!", description=(f"{user} was  removed from the blacklist by {ctx.author.mention}, \n with the reason : {reason}!"), color=0x12e612)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    def read_json(filename):
        with open(f"./config/{filename}.json", "r") as file:
            data = json.load(file)
        return data

    @commands.Cog.listener()
    def write_json(filename):
        with open(f"config/{filename}.json", "w") as file:
            json.dump(data, file, indent=4)

def setup(client):
    client.add_cog(Botdev(client))