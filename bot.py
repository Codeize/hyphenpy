import discord
import time
import asyncio

messages = joined = 0

def read_token():
    with open("token.txt.", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


token = read_token()

client = discord.Client()


async def update_stats():
    await client.wait_until_ready()
    global messages, joined

    while not client.is_closed():
        try:
            with open("stats.txt", "a") as f:
                f.write(f"Time: {int(time.time())}, Messages : {messages}, Members Joined : {joined}\n")

            messages = 0
            joined = 0

            await asyncio.sleep(60)
        except Exception as e:
            print(e)
            await asyncio.sleep(60)



@client.event
async def on_member_join(member):
   global joined
   joined += 1
   for channel in member.guild.channels:
     if str(channel) == "👋-welcome":
       await channel.send(f"""Welcome to the server, {member.mention}! Don't forget to read the <#738852223236177980> channel! And most importantly, have fun!""")


@client.event
async def on_message(message):
    global messages
    messages += 1
    if message.author.bot:
        return
    id = client.get_guild(728356912634134628)
    channels = ["💻-bot-commands", "hyphen-bot-testing", "staff-bot-commands", "helpers", "mods", "admins", "✅-general"]
    bad_words = ["fag", "cunt", "retard", "wanker"]

    for word in bad_words:
     if message.content.count(word) > 0:
      await message.channel.purge(limit=1)
      await message.channel.send(f"{message.author.mention}, that word isn't allowed here!")
      if message.author.bot:
         return

    if message.content == "-help":
        hembed = discord.Embed(title="Need help?", description="I'm here to help!")
        hembed.add_field(name="-hello", value="Says Hello back to the user.")
        hembed.add_field(name="-users", value="Prints the amount of users currently in the server.")
        await message.channel.send(content=None, embed=hembed)

    if str(message.channel) in channels:
        if message.content.find("-hello") != -1:
            await message.channel.send("Hi," + " " + message.author.name + "! :wave:")
        elif message.content == "-users":
            await message.channel.send(f"""Number of members currently in the server : {id.member_count}""")
    else:
        print(f"""User : {message.author} tried to do command : {message.content}, in channel {message.channel}""")


client.loop.create_task(update_stats())
client.run(token)
