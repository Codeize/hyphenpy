import discord
from discord.ext import commands

client = commands.Bot(command_prefix = "-")

@client.event
async def on_ready():
    print('Hyphen is online and active.')

client.run('NzQ1NjIyMTQyNjU3MzY0MDQw.Xz0cuw.PUkr0_srpyc_ymZ8P-t0WJEwA3c')
