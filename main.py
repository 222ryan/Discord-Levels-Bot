# Version 1.8 // Requires Config 1.7

# Imports
from discord.ext import commands
from discord.ext.commands import CommandNotFound, MissingRequiredArgument, CommandInvokeError
import discord
from ruamel.yaml import YAML
import levelsys
import logging

yaml = YAML()

# Opens the config and reads it, no need for changes unless you'd like to change the library (no need to do so unless having issues with ruamel)
with open("./config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)

cogs = [levelsys]

# Command Prefix + Removes the default discord.py help command
client = commands.Bot(command_prefix=config['Prefix'], intents=discord.Intents.all(), case_insensitive=True)
client.remove_command('help')

if config['enable_log'] is True:
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='logs.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)


@client.event  # On Bot Startup, Will send some details about the bot, feel free to remove the print messages, but keep everything else.
async def on_ready():
    config_status = config['bot_status_text']
    config_activity = config['bot_activity']
    activity = discord.Game(name=config['bot_status_text'])
    print('------')
    print('Logged In:')
    print(f"Bot Username: {client.user.name}\nBotID: {client.user.id}")
    print('------')
    print(f"Set Status To: {config_status}\nSet Activity To: {config_activity}")
    print("------")

    await client.change_presence(status=config_activity, activity=activity)


@client.event  # Stops Certain errors from being thrown in the console (Don't remove as it'll cause command error messages to not send!)
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    if isinstance(error, MissingRequiredArgument):
        return
    if isinstance(error, CommandInvokeError):
        return
    raise error


for i in range(len(cogs)):
    cogs[i].setup(client)


client.run(config['Bot_Token'])
