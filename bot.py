from discord.ext import commands
import sys, os
from misc.injectENV import bang
import glob

client = commands.Bot(command_prefix="-", description="Sparse, rewritten in python for better functionality")
bang()
@client.event
async def on_ready():
    print(f"[Client] {client.user.name} has connected to the discord API.")
    try:
        client.load_extension('cogs.misc')
        client.load_extension('cogs.fun')
    except Exception as e:
        print(e)

client.run(os.getenv('token'))
