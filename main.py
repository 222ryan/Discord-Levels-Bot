from discord.ext import commands
from discord.ext.commands import CommandNotFound
import discord
from ruamel.yaml import YAML
import levelsys

yaml = YAML()

with open("./config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)

cogs = [levelsys]

client = commands.Bot(command_prefix=config['Prefix'], intents=discord.Intents.all(), case_insensitive=True)
client.remove_command('help')


@client.event
async def on_ready():
    configactivity = config['bot_activity']
    activity = discord.Game(name=config['bot_status_text'])
    await client.change_presence(status=configactivity, activity=activity)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error

for i in range(len(cogs)):
    cogs[i].setup(client)

client.run(config['Bot_Token'])
