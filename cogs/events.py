import discord
from discord.ext import commands
import random
import datetime

servers = 8

class Events(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} has been loaded\n-----")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # On member joins we find a channel called general and if it exists,
        # send an embed welcoming them to our guild
        channel = discord.utils.get(member.guild.text_channels, id="764513669706022912")
        if channel:
            embed = discord.Embed(description=(f"Welcome to the server, {member.mention}. Enjoy your stay!"), color=0x42cef5)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_author(name=member.name, icon_url=member.avatar_url)
            embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
            embed.timestamp = datetime.datetime.utcnow()

            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        # On member remove we find a channel called general and if it exists,
        # send an embed saying goodbye from our guild-
        channel = discord.utils.get(member.guild.text_channels, id="764513669706022912")
        if channel:
            embed = discord.Embed(description=(f"Farewell, {member.mention}. It was nice knowing you!"), color=0x42cef5)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_author(name=member.name, icon_url=member.avatar_url)
            embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
            embed.timestamp = datetime.datetime.utcnow()

            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        #Ignore these errors
        ignored = (commands.CommandNotFound, commands.UserInputError)
        if isinstance(error, ignored):
            return

        if isinstance(error, commands.CommandOnCooldown):
            # If the command is currently on cooldown trip this
            m, s = divmod(error.retry_after, 60)
            h, m = divmod(m, 60)
            if int(h) == 0 and int(m) == 0:
                await ctx.send(f" You must wait {int(s)} seconds to use this command!")
            elif int(h) == 0 and int(m) != 0:
                await ctx.send(f" You must wait {int(m)} minutes and {int(s)} seconds to use this command!")
            else:
                await ctx.send(f" You must wait {int(h)} hours, {int(m)} minutes and {int(s)} seconds to use this command!")
        elif isinstance(error, commands.CheckFailure):
            # If the command has failed a check, trip this
            embed = discord.Embed(title="Error!",description=(f"Hey! {ctx.author.mention}, you don't have permission to use this command!"), color=0x42cef5)
            await ctx.send(embed=embed)
        raise error

    @commands.Cog.listener()
    async def on_guild_join(guild):
        servers = servers+1
        channel = self.client.get_channel(774940408618418186)

        embed = discord.Embed(title="New Server!", description=(f"Hyphen was added to {guild.name}! New Server Count : **{servers}**!"), color=0x31e30e)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_leave(guild):
        servers = servers-1
        channel = self.client.get_channel(774940408618418186)

        embed = discord.Embed(title="Minus Server!", description=(f"Hyphen was removed from {guild.name} :( - New Server Count : **{servers}**!"), color=0x31e30e)
        await channel.send(embed=embed)


def setup(client):
    client.add_cog(Events(client))