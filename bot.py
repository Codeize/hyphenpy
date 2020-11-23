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
from AntiSpam import AntiSpamHandler

# DB
from utils.mongo import Document

# error color = ff0000
# successful color = 31e30e

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")

warn_embed_dict = {
    "title": "**Hey $USERNAME!**",
    "description": "Please refrain from spamming! ~~It's not cool smh.~~",
    "timestamp": True,
    "color": 0xFF0000,
    "footer": {"text": "$BOTNAME", "icon_url": "$BOTAVATAR"},
    "author": {"name": "$GUILDNAME", "icon_url": "$GUILDICON"},
    "fields": [
        {"name": "Current warns:", "value": "$WARNCOUNT", "inline": False},
        {"name": "Current kicks:", "value": "$KICKCOUNT", "inline": False},
    ],
}

guild_kick_embed_dict = {
    "title": "**$USERNAME was kicked!**",
    "description": "$USERNAME was kicked for excessive spamming!",
    "timestamp": True,
    "color": 0xFF0000,
    "footer": {"text": "$BOTNAME", "icon_url": "$BOTAVATAR"},
    "author": {"name": "$GUILDNAME", "icon_url": "$GUILDICON"},
    "fields": [
        {"name": "Current warns:", "value": "$WARNCOUNT", "inline": False},
        {"name": "Current kicks:", "value": "$KICKCOUNT", "inline": False},
    ],
}

guild_ban_embed_dict = {
    "title": "**$USERNAME was banned!**",
    "description": "$USERNAME was banned permanentely for excessive spamming!",
    "timestamp": True,
    "color": 0xFF0000,
    "footer": {"text": "$BOTNAME", "icon_url": "$BOTAVATAR"},
    "author": {"name": "$GUILDNAME", "icon_url": "$GUILDICON"},
    "fields": [
        {"name": "Current warns:", "value": "$WARNCOUNT", "inline": False},
        {"name": "Current kicks:", "value": "$KICKCOUNT", "inline": False},
    ],
}

user_kick_embed_dict = {
    "title": "**$USERNAME, you were kicked!**",
    "description": "You were kicked from $GUILDNAME because you were spamming!",
    "timestamp": True,
    "color": 0xFF0000,
    "footer": {"text": "$BOTNAME", "icon_url": "$BOTAVATAR"},
    "author": {"name": "$GUILDNAME", "icon_url": "$GUILDICON"},
    "fields": [
        {"name": "Current warns:", "value": "$WARNCOUNT", "inline": False},
        {"name": "Current kicks:", "value": "$KICKCOUNT", "inline": False},
    ],
}

user_ban_embed_dict = {
    "title": "**$USERNAME, you were banned!**",
    "description": "You were banned from $GUILDNAME because you were spamming!",
    "timestamp": True,
    "color": 0xFF0000,
    "footer": {"text": "$BOTNAME", "icon_url": "$BOTAVATAR"},
    "author": {"name": "$GUILDNAME", "icon_url": "$GUILDICON"},
    "fields": [
        {"name": "Current warns:", "value": "$WARNCOUNT", "inline": False},
        {"name": "Current kicks:", "value": "$KICKCOUNT", "inline": False},
    ],
}

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

intents = discord.Intents.all()
secret_file = json.load(open(cwd+'/bot_config/secrets.json'))
client = commands.Bot(command_prefix = get_prefix, case_insensitive=True, help_command=None, owner_id=668423998777982997, intents=intents)
client.handler = AntiSpamHandler(client, 1, ban_threshold=10, kick_threshold=5, message_interval=15000, ignore_bots=False, guild_warn_message=warn_embed_dict, guild_kick_message=guild_kick_embed_dict, guild_ban_message=guild_ban_embed_dict, user_kick_message=user_kick_embed_dict, user_ban_message=user_ban_embed_dict)
client.config_token = secret_file['token']
client.connection_url = secret_file["mongo"]
logging.basicConfig(level=logging.INFO)
client.joke_api_key = secret_file["x-rapidapi-key"]

client.cwd = cwd
client.muted_users = {}

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
            print(f"{guild.name} \n-----")
        except UnicodeEncodeError:
            print("Guild name contains unicode that isn't supported. Skippiing...\n-----")

    client.mongo = motor.motor_asyncio.AsyncIOMotorClient(str(client.connection_url))
    client.db = client.mongo["hyphen"]
    client.config = Document(client.db, "config")
    client.setup = Document(client.db, "setup")
    client.mutes = Document(client.db, "mutes")
    print("Initialized Database\n-----")
    
    for document in await client.config.get_all():
        print(document)

    currentMutes = await client.mutes.get_all()
    for mute in currentMutes:
        client.muted_users[mute["_id"]] = mute

    print(client.muted_users)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="Error!", description="Error 422 - Unprocessable Input (commands.MissingRequiredArgument).", color=0xff0000)
        await ctx.send(embed=embed) 

@client.event
async def on_message(message):
    if message.author.id == client.user.id:
        return
    client.handler.propagate(message)
    await client.process_commands(message)

async def ch_pr():
    await client.wait_until_ready()

    statuses = [f"over {len(client.guilds)} servers for FREE [-invite]! | -help"]

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
