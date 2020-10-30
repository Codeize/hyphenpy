import discord
from discord.ext import commands
#import logging // COMING SOON


client = commands.Bot(command_prefix = "-", help_command=None)
#logging.basicConfig(level=logging.INFO)


@client.event
async def on_ready():
    print("Hyphen is online and active.")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="Error!", description="Oops, it seems an error occurred! \n According to what my developer told me, you forgot to add a required argument, check the help command to see what you did wrong. \n If all else fails join the [Official Support Server](https://discord.gg/KCZ36rS9g6) and someone will help you! \n Error 422 - Unprocessable Input (commands.MissingRequiredArgument).", color=0xf5141b)
        await ctx.send(embed=embed)

@client.command()
async def echo(ctx, *, message=None):
    message = message or "Please provide the message to be echoed!"
    await ctx.message.delete()
    await ctx.send(message)

@client.command()
async def kick(ctx, member : discord.Member, *, reason=None):
    embed = discord.Embed(title="User Kicked!", description=(f"User : {member.mention}, was kicked by Staff member : {ctx.message.author.mention}. \n With the reason : {reason}!"), color=0x31e30e)
    await ctx.send(embed=embed)
    await member.kick(reason=reason)

@client.command()
async def ban(ctx, member : discord.Member, *, reason="No reason was provided"):
    embed = discord.Embed(title="User Banned!", description=(f"User : {member.mention}, was banned by Staff member : {ctx.message.author.mention}. \n With the reason : {reason}!"), color=0x31e30e)
    await ctx.send(embed=embed)
    await member.ban(reason=reason)

@client.command()
async def unban(ctx, *, member):
    bannedUsers = await ctx.guild.bans()
    memberName, memberDiscriminator = member.split("#")

    for banEntry in bannedUsers:
        user = banEntry.user

        if (user.name, user.discriminator) == (user.name, user.discriminator):
            embed = discord.Embed(title="User Unbanned!", description=(f"User : {member}, was unbanned by Staff member : {ctx.message.author.mention}!"), color=0x31e30e)
            await ctx.send(embed=embed)
            await ctx.guild.unban(user)

@client.command()
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit=amount)
    embed = discord.Embed(title="Purged Message(s)!",  description=(f"Purged {amount} message(s)!"))
    await ctx.send(embed=embed)
    await ctx.message.delete()

client.run("NzQ1NjIyMTQyNjU3MzY0MDQw.Xz0cuw.PUkr0_srpyc_ymZ8P-t0WJEwA3c")
