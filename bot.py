import discord
from discord.ext import commands
#import logging // COMING SOON
import random
import asyncio
import os


client = commands.Bot(command_prefix = "-")
#logging.basicConfig(level=logging.INFO)


@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="over the Game Jam! | gj!help"))
    print("Hyphen is online and active.")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="Error!", description="Oops, it seems an error occurred! \n According to what my developer told me, you forgot to add a required argument, check the help command to see what you did wrong. \n If all else fails join the [Official Support Server](https://discord.gg/KCZ36rS9g6) and someone will help you! \n Error 422 - Unprocessable Input (commands.MissingRequiredArgument).", color=0xf5141b)
        await ctx.send(embed=embed)

async def ch_pr():
    await client.wait_until_ready()

    statuses = ["my developer developing me!", f"over {len(client.guilds)} servers! | -help", "everyone... spoooooky!"]

    while not client.is_closed():

        status = random.choice(statuses)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status))

        await asyncio.sleep(15)

client.loop.create_task(ch_pr())

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

client.run("NzQ1NjIyMTQyNjU3MzY0MDQw.Xz0cuw.PUkr0_srpyc_ymZ8P-t0WJEwA3c")
