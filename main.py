# Imports
import asyncio
from os import listdir

from discord.ext import commands
from discord.ext.commands import CommandNotFound, MissingRequiredArgument, CommandInvokeError, MissingRole, \
    NoPrivateMessage
import discord
from ruamel.yaml import YAML
import logging
import os
from dotenv import load_dotenv

load_dotenv()

# Opens the config and reads it, no need for changes unless you'd like to change the library (no need to do so unless having issues with ruamel)
yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)
with open("Configs/spamconfig.yml", "r", encoding="utf-8") as file2:
    spamconfig = yaml.load(file2)
with open("Configs/holidayconfig.yml", "r", encoding="utf-8") as file3:
    seasonconfig = yaml.load(file3)

# Command Prefix + Removes the default discord.py help command
client = commands.Bot(command_prefix=config['Prefix'], intents=discord.Intents.all(), case_insensitive=True)
client.remove_command('help')

# sends discord logging files which could potentially be useful for catching errors.
os.remove("Logs/logs.txt")
FORMAT = '[%(asctime)s]:[%(levelname)s]: %(message)s'
logging.basicConfig(filename='Logs/logs.txt', level=logging.DEBUG, format=FORMAT)
logging.debug('Started Logging')
logging.info('Connecting to Discord.')


@client.event  # On Bot Startup, Will send some details about the bot and sets it's activity and status. Feel free to remove the print messages, but keep everything else.
async def on_ready():
    config_status = config['bot_status_text']
    config_activity = config['bot_activity']
    activity = discord.Game(name=config['bot_status_text'])
    logging.info('Getting Bot Activity from Config')
    print("If you encounter any bugs, please let me know.")
    print('------')
    print('Logged In As:')
    print(f"Username: {client.user.name}\nID: {client.user.id}")
    print('------')
    print(f"Status: {config_status}\nActivity: {config_activity}")
    print('------')
    await client.change_presence(status=config_activity, activity=activity)


logging.info("------------- Loading -------------")
for fn in listdir("Commands"):
    if fn.endswith(".py"):
        logging.info(f"Loading: {fn}")
        client.load_extension(f"Commands.{fn[:-3]}")
        logging.info(f"Loaded {fn}")

for fn in listdir("Addons"):
    if fn.endswith(".py"):
        logging.info(f"Loading: {fn} Addon")
        client.load_extension(f"Addons.{fn[:-3]}")
        logging.info(f"Loaded {fn} Addon")

logging.info(f"Loading Level System")
client.load_extension("Systems.levelsys")
logging.info(f"Loaded Level System")

if spamconfig['antispam_system'] is True:
    logging.info(f"Loading Anti-Spam System")
    client.load_extension("Systems.spamsys")
    logging.info(f"Loaded Anti-Spam System")

logging.info("------------- Finished Loading -------------")

# Uses the bot token to login, so don't remove this.
token = os.getenv("DISCORD_TOKEN")
client.run(token)

# End Of Main
