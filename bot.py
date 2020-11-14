# Standard Libraries
from pathlib import Path
import os
import random
import json

# Third Party Libraries
import discord
from discord.ext import commands, buttons
import asyncio
import logging
import motor.motor_asyncio

# DB
from utils.mongo import Document


# error color = ff0000
# successful color = 31e30e

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")

async def get_prefix(client, message):
    # If dm's
    if not message.guild:
        return commands.when_mentioned_or("-")(client, message)

    try:
        data = await client.config.find(message.guild.id)

        # Make sure we have a useable prefix
        if not data or "prefix" not in data:
            return commands.when_mentioned_or("-")(client, message)
        return commands.when_mentioned_or(data["prefix"])(client, message)
    except:
        return commands.when_mentioned_or("-")(client, message)

intents = discord.Intents.all()
secret_file = json.load(open(cwd+'/bot_config/secrets.json'))
client = commands.Bot(command_prefix = get_prefix, case_insensitive=True, help_command=None, owner_id=668423998777982997)
client.config_token = secret_file['token']
client.connection_url = secret_file["mongo"]
logging.basicConfig(level=logging.INFO)
client.joke_api_key = secret_file["x-rapidapi-key"]

client.cwd = cwd

@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")

@client.event
async def on_ready():
    print("Hyphen is online and active.\n-----")
    print('Servers connected to:')
    for guild in client.guilds:
        try:
            print(guild.name + "\n-----")
        except UnicodeEncodeError:
            print("Guild name contains unicode that isn't supported. Skippiing...\n-----")

    client.mongo = motor.motor_asyncio.AsyncIOMotorClient(str(client.connection_url))
    client.db = client.mongo["hyphen"]
    client.config = Document(client.db, "config")
    print("Initialized Database\n-----")
    for document in await client.config.get_all():
        print(document)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="Error!", description="Oops, it seems an error occurred! \n According to what my developer told me, you forgot to add a required argument, check the help command to see what you did wrong. \n If all else fails join the [Official Support Server](https://discord.gg/KCZ36rS9g6) and someone will help you! \n Error 422 - Unprocessable Input (commands.MissingRequiredArgument).", color=0xff0000)
        await ctx.send(embed=embed)

@client.event
async def on_message(message):
    if message.author.id == client.user.id:
        return

    await client.process_commands(message)

async def ch_pr():
    await client.wait_until_ready()

    statuses = [f"over {len(client.guilds)} servers for FREE! | -help"]

    while not client.is_closed():

        status = random.choice(statuses)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status))

        await asyncio.sleep(15)

client.loop.create_task(ch_pr())

if __name__ == '__main__':
    # When running this file, if it is the 'main' file
    # I.E its not being imported from another python file run this
    for file in os.listdir(cwd+"/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            client.load_extension(f"cogs.{file[:-3]}")

client.run(client.config_token)
