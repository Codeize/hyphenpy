import sqlite3
from discord.ext import commands
import discord

class Welcome(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} has been loaded\n-----")

    @commands.Cog.listener()
    async def on_member_join(member):
        embed = discord.Embed(color=0x00f7ff, description=f"Welcome to {server.name}, {member}! You are member #{len(list(member.guild.members))}!")
        embed.set_thumbnail(url=f"{member.avatar_url}")
        embed.set_author(name=f"{member.name}", icon_url=f"{member.avatar_url}")
        embed.set_footer(name=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
        embed.timestamp = datetime.datetime.utcnow()

        channel = bot.get_channel(id=464568292344784378)
        await channel.send(embed=embed)

def setup(client):
    client.add_cog(Welcome(client))