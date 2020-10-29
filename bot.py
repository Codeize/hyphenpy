import discord
from discord.ext import commands
#import logging // COMING SOON
#from pathlib import paths
import json

client = commands.Bot(command_prefix = "-", help_command=None)

secret_file = json.load(open(cwd+'/bot_config/secrets.json'))
bot = commands.Bot(command_prefix='-', case_insensitive=True)
bot.config_token = secret_file['token']
#logging.basicConfig(level=logging.INFO)


@client.event
async def on_ready():
    print("Hyphen is online and active.")

@client.command()
async def echo(ctx, *, message=None):
    message = message or "Please provide the message to be echoed!"
    await ctx.message.delete()
    await ctx.send(message)

client.run(client.config_token)
