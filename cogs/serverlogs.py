from discord.ext import commands
import discord
class serverlogs(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        joinleavelogs = self.client.get_channel(816045992788623440)
        embed = discord.Embed(title="Server Gained :)",
                              description=f"Watchdog is now in {len(self.client.guilds)} servers!", color=0x00ff73)
        embed.set_footer(text="Made by Codeize#0001")
        await joinleavelogs.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        joinleavelogs = self.client.get_channel(816045992788623440)
        embed = discord.Embed(title="Server Lost :(",
                              description=f"Watchdog is now in {len(self.client.guilds)} servers!", color=0xff0000)
        embed.set_footer(text="Made by Codeize#0001")
        await joinleavelogs.send(embed=embed)

def setup(client):
    client.add_cog(serverlogs(client))