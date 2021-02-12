from discord.ext import commands
import discord
import levelsys

cogs = [levelsys]

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

for i in range(len(cogs)):
    cogs[i].setup(client)

client.run("token here")
