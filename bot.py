# Standard Libraries
from pathlib import Path
import os
import random
import json
import sqlite3

# Third Party Libraries
import discord
from discord.ext import commands
import asyncio
import logging

# Proj Modules
from database import db

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"-----\n{cwd}\n-----")

with open(cwd + "/bot_config/secrets.json") as secret_file:
    secret_file = json.load(secret_file)

owners = [668423998777982997, 671791003065384987]
intents = discord.Intents.all()
client = commands.Bot(command_prefix = "wd-", case_insensitive=True, help_command=None, owner_ids=owners, intents=intents)

client.config_token = secret_file["token"]
# logging.basicConfig(level=logging.INFO)

# Client Vars
client.cwd = cwd
client.muted_users = {}

client.e_colour = 0xff0000
client.s_colour = 0x31e30e

client.statuses = [f"over {len(client.guilds)} servers for FREE [wd-invite]! | wd-help"]

db()

@client.event
async def on_ready():
    db = sqlite3.connect('wd.sqlite')
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS main(
        guild_id TEXT,
        message TEXT,
        channel_id TEXT
        )
    ''')
    print("__MAIN INFO__\n-----\nWatchdog is online and active. --- (https://watchdog.tk)\nDeveloped by https://codeize.dev/\n*(C) Codeize 2021 ALL RIGHTS RESERVED*\n-----\n")
    print(f"__SERVERS__\n-----\nConnected to {len(client.guilds)} servers\n-----")
    print('Servers connected to:\n-----')
    for guild in client.guilds:
        try:
            print(f"{guild.name} \n-----")
        except UnicodeEncodeError:
            print("Guild name contains unicode that isn't supported. Skippiing...\n-----")

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
