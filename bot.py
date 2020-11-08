import discord
from discord.ext import commands
from pathlib import Path
import random
import asyncio
import os
import json
import cogs._json

# error color = ff0000
# successful color = 31e30e

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")

def get_prefix(client, message):
    data = cogs._json.read_json('prefixes')
    if not str(message.guild.id) in data:
        return commands.when_mentioned_or('-')(client, message)
    return commands.when_mentioned_or(data[str(message.guild.id)])(client, message)

client = commands.Bot(command_prefix = get_prefix, case_insensitive=True, owner_id=668423998777982997)

client.blacklisted_users = []
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

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="Error!", description="Oops, it seems an error occurred! \n According to what my developer told me, you forgot to add a required argument, check the help command to see what you did wrong. \n If all else fails join the [Official Support Server](https://discord.gg/KCZ36rS9g6) and someone will help you! \n Error 422 - Unprocessable Input (commands.MissingRequiredArgument).", color=0xff0000)
        await ctx.send(embed=embed)

@client.event
async def on_message(message):
    if message.author.id == client.user.id:
        return

    if message.author.id in client.blacklisted_users:
        return

    if f"<@!{client.user.id}>" in message.content:
        data = cogs._json.read_json('prefixes')
        if str(message.guild.id) in data:
            prefix = data[str(message.guild.id)]
        else:
            prefix = '-'
        prefixMsg = await message.channel.send(f"My prefix here is `{prefix}`")
        await prefixMsg.add_reaction('👀')

    await client.process_commands(message)

async def ch_pr():
    await client.wait_until_ready()

    statuses = ["my developer developing me!", f"over {len(client.guilds)} servers for FREE! | -help", "Netflix and vibing to music!"]

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

client.run("NzQ1NjIyMTQyNjU3MzY0MDQw.Xz0cuw.PUkr0_srpyc_ymZ8P-t0WJEwA3c")
