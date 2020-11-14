import discord
from discord.ext import commands
import random

class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} has been loaded\n-----")

    @commands.command(name="echo", description="Echos the message provdied")
    async def echo(self, ctx, *, message=None):
        message = message or "Please provide the message to be echoed!"
        await ctx.message.delete()
        await ctx.send(message)

    @commands.command(name="8 ball", aliases=["8ball"], desc="Ask me a question and.. *I will decide your fate...*")
    async def _8ball(self, ctx, *, question):
        responses = ["It is certain.",

"It is decidedly so.",

"Without a doubt.",

"Yes - definitely.",

"You may rely on it.",

"As I see it, yes.",

"Most likely.",

"Outlook good.",

"Yes.",

"Signs point to yes.",

"Reply hazy, try again.",

"Ask again later.",

"Better not tell you now.",

"Cannot predict now.",

"Concentrate and ask again.",

"Don't count on it.",

"My reply is no.",

"My sources say no.",

"Outlook not so good.",

"Very doubtful."]
        await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")


def setup(client):
    client.add_cog(Misc(client))