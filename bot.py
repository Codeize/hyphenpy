import discord
from discord.ext import commands
import random
import asyncio
import os

# error color = ff0000
# successful color = 31e30e

client = commands.Bot(command_prefix = "-")

@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")

@client.event
async def on_ready():
    print("Hyphen is online and active.")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="Error!", description="Oops, it seems an error occurred! \n According to what my developer told me, you forgot to add a required argument, check the help command to see what you did wrong. \n If all else fails join the [Official Support Server](https://discord.gg/KCZ36rS9g6) and someone will help you! \n Error 422 - Unprocessable Input (commands.MissingRequiredArgument).", color=0xff0000)
        await ctx.send(embed=embed)

async def ch_pr():
    await client.wait_until_ready()

    statuses = ["my developer developing me!", f"over {len(client.guilds)} servers for FREE! | -help", "everyone... spoooky!"]

    while not client.is_closed():

        status = random.choice(statuses)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status))

        await asyncio.sleep(15)

client.loop.create_task(ch_pr())

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

client.run("NzQ1NjIyMTQyNjU3MzY0MDQw.Xz0cuw.PUkr0_srpyc_ymZ8P-t0WJEwA3c")
