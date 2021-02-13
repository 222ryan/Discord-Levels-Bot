from discord.ext import commands
import discord
from ruamel.yaml import YAML
import levelsys

yaml = YAML()

with open("./config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)

cogs = [levelsys]

client = commands.Bot(command_prefix=config['Prefix'], intents=discord.Intents.all())
client.remove_command('help')

for i in range(len(cogs)):
    cogs[i].setup(client)

client.run(config['Bot_Token'])
