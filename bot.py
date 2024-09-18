import discord
import os

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guild_messages = True
intents.guilds = True

client = discord.Client(intents=intents)

async def init():
    await client.start(os.environ["TOKEN"]) 

@client.event
async def on_ready():
    print(f"logged in as {client.user}")

@client.event
async def on_message(message: discord.Message):
    if message.channel.id != int(os.environ["CHANNEL_ID"]):
        return

    if not message.content.startswith("!"):
        return

    split = message.content.split(" ")

    if split[0] == "!add":
        await add_search_term(message)
    elif split[0] == "!remove":
        await remove_search_term(message)
 
async def add_search_term(message: discord.Message):
    search_term = message.content.split("!add")[1].strip()

    with open("./config/search_terms.txt", "a") as f:
        f.writelines(search_term+"\n")

    await message.reply(":white_check_mark: done")

async def remove_search_term(message: discord.Message):
    search_term = message.content.split("!remove")[1].strip()
    
    with open("./config/search_terms.txt", "r") as f:
        lines = f.readlines()
    with open("./config/search_terms.txt", "w") as f:
        if search_term + "\n" not in lines:
            await message.reply(":x: search term does not exist")
            return

        for line in lines:
            if line == search_term+"\n":
                continue
            f.write(line)

    await message.reply(":white_check_mark: done")

async def send_alert(job_title: str, job_description: str, url: str):
    await client.wait_until_ready()

    channel = client.get_channel(int(os.environ["CHANNEL_ID"]))

    if channel is None:
        channel = await client.fetch_channel(int(os.environ["CHANNEL_ID"]))

    if not isinstance(channel, discord.TextChannel):
        raise TypeError("channel is not of type TextChannel")

    embed = discord.Embed(
        title=job_title,
        url=url,
        description=job_description,
        color=0xb6fc03
    )

    await channel.send(embed=embed)
