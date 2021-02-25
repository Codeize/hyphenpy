# Standard Libraries
from pathlib import Path
import os
import random
import json

# Third Party Libraries
import discord
from discord.ext import commands
import asyncio
import logging

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")

async def get_prefix(client, message):
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

with open(cwd + "/bot_config/secrets.json") as secret_file:
    secret_file = json.load(secret_file)

owners = [668423998777982997, 671791003065384987]
intents = discord.Intents.all()
client = commands.Bot(command_prefix = get_prefix, case_insensitive=True, help_command=None, owner_ids=owners, intents=intents)

client.config_token = secret_file["token"]
logging.basicConfig(level=logging.INFO)

# Client Vars
client.cwd = cwd
client.muted_users = {}

client.e_colour = 0xff0000
client.s_colour = 0x31e30e

client.statuses = [f"over {len(client.guilds)} servers for FREE [-invite]! | -help"]

@client.event
async def on_ready():
    print("Watchdog is online and active.")
    print(f"Connected to {len(client.guilds)} servers")

    # No database stuff here no more
    # Or mutes or the other thing

@client.event
async def on_message(message):
    if message.author.id == client.user.id:
        return
    if message.author.bot:
        return
    await client.process_commands(message)

async def ch_pr():
    await client.wait_until_ready()
    while not client.is_closed():
        status = random.choice(client.statuses)
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
