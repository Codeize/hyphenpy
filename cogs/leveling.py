import sqlite3
from discord.ext import commands
import discord
import math

class Leveling(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} has been loaded\n-----")

    @commands.Cog.listener()
    async def on_message(self, message):
        db = sqlite3.connect('wd.sqlite')
        cursor = db.cursor()
        cursor.execute("SELECT setting FROM modules WHERE guild_id=?", (message.guild.id,))
        setting = bool(cursor.fetchone()[0])
        if setting:
            return
        else:
            db = sqlite3.connect('wd.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT user_id FROM levels WHERE guild_id = '{message.guild.id}' and user_id  = '{message.author.id}'")
            result = cursor.fetchone()
            if result is None:
                sql  = ("INSERT INTO levels(guild_id, user_id, exp, lvl) VALUES(?,?,?,?)")
                val = (message.author.guild.id, message.author.id, 2, 0)
                cursor.execute(sql, val)
                db.commit()
            else:
                cursor.execute(f"SELECT user_id, exp, lvl FROM levels WHERE guild_id = '{message.guild.id}' and user_id = '{message.author.id}'")
                result1 = cursor.fetchone()
                exp = int(result1[1])
                sql = ("UPDATE levels SET exp = ? WHERE guild_id = ? and user_id = ?")
                val = (exp + 2, str(message.guild.id), str(message.author.id))
                cursor.execute(sql, val)
                db.commit()

                cursor.execute(f"SELECT user_id, exp, lvl FROM levels WHERE guild_id = '{message.guild.id}' and user_id = '{message.author.id}'")
                result2 = cursor.fetchone()

                xp_start = int(result2[1])
                lvl_start = int(result2[2])
                xp_end = math.floor(5 * (lvl_start ^ 2) + 50 * lvl_start + 100)
                if xp_end < xp_start:
                    await message.channel.send(f"{message.author.mention} ranked up to level {lvl_start + 1}!")
                    sql = ("UPDATE levels SET lvl = ? WHERE guild_id = ? and user_id = ?")
                    val = (int(lvl_start + 1), str(message.guild.id), str(message.author.id))
                    cursor.execute(sql, val)
                    db.commit()
                    sql = ("UPDATE levels SET exp = ? WHERE guild_id = ? and user_id = ?")
                    val = (0, str(message.guild.id), str(message.author.id))
                    db.commit()
                    cursor.close()
                    db.close()

    @commands.command()
    async def rank(self, ctx, user:discord.User=None):
        if user is not None:
            db = sqlite3.connect('wd.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT user_id, exp, lvl FROM levels WHERE guild_id = '{ctx.message.guild.id}' and user_id = '{user.id}'")
            result = cursor.fetchone()
            if result is None:
                await ctx.send("That user isn't ranked yet!")
            else:
                await ctx.send(f"{user.name} is currently level `{str(result[2])}` and has `{str(result[1])}` XP!")
            cursor.close()
            db.close()
        elif user is None:
            db = sqlite3.connect('wd.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT user_id, exp, lvl FROM levels WHERE guild_id = '{ctx.message.guild.id}' and user_id = '{ctx.message.author.id}'")
            result = cursor.fetchone()
            if result is None:
                await ctx.send("That user isn't ranked yet!")
            else:
                await ctx.send(f"{ctx.message.author.name} is currently level `{str(result[2])}` and has `{str(result[1])}` XP!")
                cursor.close()
                db.close()

    @commands.command()
    async def disable_lvl(self, ctx):
        db = sqlite3.connect('wd.sqlite')
        cursor = db.cursor()
        sql = ("INSERT INTO modules(guild_id, setting, module_name) VALUES(?,?,?)")
        val = (ctx.guild.id, 1, "leveling")
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        await ctx.send("up to now all g")

def setup(client):
    client.add_cog(Leveling(client))