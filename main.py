# Imports
from discord.ext import commands
from discord.ext.commands import CommandNotFound, MissingRequiredArgument, CommandInvokeError, MissingRole
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


# Command Prefix + Removes the default discord.py help command
client = commands.Bot(command_prefix=config['Prefix'], intents=discord.Intents.all(), case_insensitive=True)
client.remove_command('help')

# sends discord logging files which could potentially be useful for catching errors.
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
    print('Logged In:')
    print(f"Bot Username: {client.user.name}\nBotID: {client.user.id}")
    print('------')
    print(f"Set Status To: {config_status}\nSet Activity To: {config_activity}")
    print("------")
    print("Started System: Levels")
    await client.change_presence(status=config_activity, activity=activity)
    logging.info('Logged In And Set Activity')


@client.event  # Stops Certain errors from being thrown in the console (Don't remove as it'll cause command error messages to not send! - Only remove if adding features and needed for testing (Don't forget to re-add)!)
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        logging.error('Command Not Found')
        return
    if isinstance(error, MissingRequiredArgument):
        logging.error('Argument Error - Missing Arguments')
        return
    if isinstance(error, CommandInvokeError):
        logging.error('Command Invoke Error')
        return
    if isinstance(error, MissingRole):
        logging.error('A user has missing roles!')
        return
    if isinstance(error, KeyError):
        logging.error('Key Error')
        return
    raise error

logging.info('Checking if anti-spam is enabled')
if spamconfig['antispam_system'] is True:
    client.load_extension("Systems.spamsys")
    logging.info('Loaded AntiSpam')
logging.info('Checking if help is enabled')
if config['help_command'] is True:
    client.load_extension("Commands.help")
    logging.info('Loaded Help Command')
client.load_extension("Systems.levelsys")
logging.info('Loaded Levelsys')
client.load_extension("Commands.rank")
logging.info('Loaded Rank Command')
client.load_extension("Commands.leaderboard")
logging.info('Loaded Leaderboard Command')
client.load_extension("Commands.background")
logging.info('Loaded Background Command')
client.load_extension("Commands.reset")
logging.info('Loaded Reset Command')
client.load_extension("Commands.circlepic")
logging.info('Loaded Circlepic Command')
client.load_extension("Commands.xpcolour")
logging.info('Loaded XPColour Command')
client.load_extension("Commands.fix")
logging.info('Loaded Fix Command')
client.load_extension("Commands.role")
logging.info('Loaded Role Command')
client.load_extension("Commands.doublexp")
logging.info('Loaded DoubleXP Command')
client.load_extension("Commands.levelchannel")
logging.info('Loaded LevelChannel Command')
client.load_extension("Commands.xppermessage")
logging.info('Loaded XPPerMessage Command')

# Uses the bot token to login, so don't remove this.
token = os.getenv("DISCORD_TOKEN")
client.run(token)

# End Of Main
