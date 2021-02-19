# Version 1.7 // Requires Config 1.4

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
    print('------')
    print('Online! Details:')
    print(f"Bot Username: {client.user.name}")
    print(f"BotID: {client.user.id}")
    print('------')

    config_status = config['bot_status_text']
    config_activity = config['bot_activity']
    print(f"Set Status: {config_status}")
    activity = discord.Game(name=config['bot_status_text'])
    print(f"Set Activity: {config_activity}")
    print("------")
    await client.change_presence(status=config_activity, activity=activity)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error

for i in range(len(cogs)):
    cogs[i].setup(client)


client.run(config['Bot_Token'])
