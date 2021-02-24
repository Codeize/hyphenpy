# Standard Libraries
import json
import io
import re

# Third Party Libraries
from discord.ext import commands
import discord
from utils.util import clean_code
from traceback import format_exception
from dbfn import reactionbook
import textwrap
import traceback
import contextlib

class Botdev(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"\n__COGS__\n{self.__class__.__name__} has been loaded\n-----")

    @commands.command(name="Shutdown", description="(Bot Developer Only!) Terminates Hyphens current session.")
    @commands.is_owner()
    async def shutdown(self, ctx):
        embed = discord.Embed(title="Logged Out!", description="Ok. Process successfully voided. - (Code 0)", color=0x12e612)
        await ctx.send(embed=embed)
        await self.client.logout()

    #@commands.command(name="Blacklist", description="(Bot Developer Only!) Blacklists the specified user.")
    #@commands.is_owner()
    #async def blacklist(self, ctx, user: discord.Member, *, reason="No reason was provided"):
    #   if ctx.message.author.id == user.id:
    #       await ctx.send("Really? You cannot blacklist yourself stoopid!")
    #       return
    


#@commands.command(name="Blacklist", description="(Bot Developer Only!) Blacklists the specified user.")
#@commands.is_owner()
#async def blacklist(self, ctx, user: discord.Member, *, reason="No reason was provided"):
##if ctx.message.author.id == user.id:
###await ctx.send("Really? You cannot blacklist yourself stoopid!")
###return

    #   self.client.blacklisted_users.append(user.id)
    #   data = cogs._json.read_json("blacklist")
    #   data["blacklistedUsers"].append(user.id)
    #   cogs._json.write_json(data, "blacklist")
    #   embed = discord.Embed(title="User Blacklisted!", description=(f"User : {user.mention}, was blacklisted by Codeize. \n With the reason : {reason}!"), color=0x31e30e)
    #   await ctx.send(embed=embed)

    #@commands.command(name="Unblacklist", description="(Bot Developer Only!) Unblacklists the specified blacklisted user.")
    #@commands.is_owner()
    #async def unblacklist(self, ctx, user: discord.Member, *, reason="No reason was provided"):
    #   self.client.blacklisted_users.remove(user.id)
    #   data = cogs._json.read_json("blacklist")
    #   data["blacklistedUsers"].remove(user.id)
    #   cogs._json.write_json(data, "blacklist")
    #   embed = discord.Embed(title="User Unblacklisted!", description=(f"User : {user.mention}, was unblacklisted by Codeize. \n With the reason : {reason}!"), color=0x31e30e)
    #   await ctx.send(embed=embed)

    #@commands.command()
    #@commands.is_owner()
    #async def dev(self, ctx):
    #   embed = discord.Embed(title="Entered Dev Mode!", description=(f"Port : **8080** Version : **0.0.3**."), color=0x31e30e)
    #   await ctx.send(embed=embed)
    #   await ctx.send("THIS IS A DEVELOPMENT BUILD OF HYPHEN!\nALL FEATURES MAY NOT PERFORM AS INTENDED!")


    @commands.command(name="load", description="[BOT DEV ONLY!] Load cog.")
    @commands.is_owner()
    async def load(self, ctx, extension):
        self.client.load_extension(f"cogs.{extension}")

    @commands.command(name="unload", description="[BOT DEV ONLY!] Unload cog.")
    @commands.is_owner()
    async def unload(self, ctx, extension):
        self.client.unload_extension(f"cogs.{extension}")


    @commands.command(
        name="reload",
        description="[BOT DEV ONLY!] Reload all/one of the bots cogs!",
        usage="[cog]",
        )
    @commands.is_owner()
    async def reload(self, ctx, cog=None):
        if not cog:
            async with ctx.typing():
                embed = discord.Embed(
                    title="Reloading all cogs!",
                    color=0x808080,
                    timestamp=ctx.message.created_at,
                    )
                description = ""
                for ext in os.listdir("./cogs/"):
                    if ext.endswith(".py") and not ext.startswith("_"):
                        try:
                            self.client.unload_extension(f"cogs.{ext[:-3]}")
                            await asyncio.sleep(0.5)
                            self.client.load_extension(f"cogs.{ext[:-3]}")
                            description += f"Reloaded: `{ext}`\n"
                        except Exception as e:
                            embed.add_field(
                                name=f"Failed to reload: `{ext}`",
                                value=e,
                            )
                    await asyncio.sleep(0.5)
                embed.description = description
                await ctx.send(embed=embed)
        else:
            async with ctx.typing():
                embed = discord.Embed(
                    title=f"Reloading {cog}!",
                    color=0x808080,
                    timestamp=ctx.message.created_at,
                )
                cog = cog.lower()
                ext = f"{cog}.py"
                if not os.path.exists(f"./cogs/{ext}"):
                    embed.add_field(
                        name=f"Failed to reload: `{ext}`",
                        value="This cog file does not exist.",
                    )
                elif ext.endswith(".py") and not ext.startswith("_"):
                    try:
                        self.client.unload_extension(f"cogs.{ext[:-3]}")
                        await asyncio.sleep(0.5)
                        self.client.load_extension(f"cogs.{ext[:-3]}")
                        embed.description = f"Reloaded: `{ext}`"
                    except Exception:
                        desired_trace = traceback.format_exc()
                        embed.add_field(
                            name=f"Failed to reload: `{ext}`",
                            value=desired_trace,
                        )
                await asyncio.sleep(0.5)
            await ctx.send(embed=embed)

    @commands.command(name="eval", description="[BOT DEV ONLY!] Evaluate given code.", aliases=["exec"])
    @commands.is_owner()
    async def _eval(self, ctx, *, code):
        """
        Evaluates given code.
        """
        code = clean_code(code)

        channel = ctx.channel,
        author = ctx.author
        guild = ctx.guild
        message = ctx.message

        book = reactionbook(self.client, ctx, TITLE="Eval")
        
        wrapped = eval("textwrap.indent(code, '    ')")
        try:
            result = str(eval(wrapped))
        except Exception as e:
            result = "".join(format_exception(e, e, e.__traceback__))

        pages = []
        wrapped = f"Input:\n```py\n{wrapped}```\n"
        for i in range(0, len(result), 2000):
            pages.append(f"Output:\n```py\n{result[i : i + 2000]}\n```")
        if len(wrapped + pages[0]) > 2000:
            pages.insert(0, wrapped)
        else:
            pages[0] = wrapped + pages[0]
        book.createpages(pages, ITEM_PER_PAGE=True)

        await book.createbook(MODE="arrows", COLOUR=self.client.s_colour,
                              TIMEOUT=180)

def setup(client):
    client.add_cog(Botdev(client))
