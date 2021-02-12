from discord.ext import commands
import discord
import levelsys

# Config - More options in levelsys.py!
prefix = "!"  # Sets the bots prefix
bot_token = ""  # Your discord application token

cogs = [levelsys]

client = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())

for i in range(len(cogs)):
    cogs[i].setup(client)

client.run(bot_token)
