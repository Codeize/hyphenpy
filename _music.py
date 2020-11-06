#import discord
#import youtube_dl
#from discord.ext import commands

#class Music(commands.Cog):

#def __init__(self, client):
##self.client = client

#@commands.Cog.listener()
#async def on_ready(self):
##print("Music is successfully loaded.")

#@commands.command()
#async def join(self, ctx):
##connected = ctx.author.voice
##if connected:
###await connected.channel.connect()
###embed = discord.Embed(title="Let's Vibe!", description=(f"Successfully joined the VC! Play some tunes, {ctx.message.author.mention}!"), color=0x31e30e)
###await ctx.send(embed=embed)

###server = ctx.message.guild
###voice_channel = server.voice_client

###async with ctx.typing():
####player = await YTDLSource.from_url(queue[0], loop=client.loop)
####voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

###await ctx.send('**Now playing:** {}'.format(player.title))
##else:
###embed = discord.Embed(title="Error!", description=(f"Hey {ctx.author.mention}! Unfortunately I can't connect to your VC, this could be one of 3 reasons : \n 1.) You are not in the VC you would like me to connect to, \n 2.) I don't have permission to connect to the VC, or, \n 3.) This part of the bot is currently down for maintenance. \n Sorry for any inconvenience!"), color=0xff0000)
###await ctx.send(embed=embed)

#@commands.command()
#async def leave(self, ctx):
##voice_client = ctx.message.guild.voice_client
##await voice_client.disconnect()
##embed = discord.Embed(title="See ya!", description=(f"Successfully disconnected from the VC! Thanks for choosing Hyphen!"), color=0x31e30e)
##await ctx.send(embed=embed)

#def setup(client):
#client.add_cog(Music(client))