import discord
from discord.ext import commands
import json
import os
import random

class Economy(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} has been loaded\n-----")

    async def account_new(self, user):
        if str(user,id) in users:
                return False
        else:
            users[str(user.id)] = {}
            users[str(user.id)]["wallet"] = 0
            users[str(user.id)]["bank"] = 0

        with open("bank.json", "w") as f:
            json.dump(users, f)
        return True

    async def get_bank_data(self):
        with open("bank.json", "r") as f:
            users = json.load(f)

        return users

    @commands.command()
    async def balance(self, ctx):
        await self.account_new(ctx.author)
        user = ctx.author

        users = await self.get_bank_data()
        wallet_amount = users[str(user.id)]["wallet"]
        bank_amount = users[str(user.id)]["bank"]

        embed = discord.Embed(title=f"{ctx.author.name}'s Balance", color=ctx.author.color)
        embed.add_field(name = "Wallet", value= wallet_amount)
        embed.add_field(name = "Bank", value= bank_amount)
        await ctx.send(embed=embed)

    @commands.command()
    async def beg(self, ctx):
        await self.account_new(ctx.author)
        user = ctx.author

        users = await self.get_bank_data()

        earnings = random.randrange(101)

        await ctx.send(f"Some good person gave you {earnings} coins!")

        users[str(user.id)]["wallet"] += earnings

        with open("bank.json", "w") as f:
            json.dump(users, f)

def setup(client):
    client.add_cog(Economy(client))