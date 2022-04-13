# Imports
import sqlite3
from os import listdir

import ruamel.yaml.error
from discord.ext import commands, ipc
from discord.ext.commands import CommandNotFound, RoleNotFound, MemberNotFound
import discord
from ruamel.yaml import YAML
import logging
import os
from dotenv import load_dotenv
import warnings
import pyfiglet


load_dotenv()

class client(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ipc = ipc.Server(self, secret_key="ModernLevels")

    async def on_ipc_error(self, endpoint, error):
        print(f"IPC Error: {endpoint} raised {error}")


# Opens the config and reads it, no need for changes unless you'd like to change the library (no need to do so unless having issues with ruamel)
yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)

warnings.simplefilter('ignore', ruamel.yaml.error.UnsafeLoaderWarning)

# Command Prefix + Removes the default discord.py help command
Client = client(command_prefix=commands.when_mentioned_or(config['Prefix']), intents=discord.Intents.all(), case_insensitive=True)
Client.remove_command('help')

# sends discord logging files which could potentially be useful for catching errors.
os.close(os.open("Logs/logs.txt", os.O_CREAT))
os.truncate("Logs/logs.txt", 1)
FORMAT = '[%(asctime)s]:[%(levelname)s]: %(message)s'
logging.basicConfig(filename='Logs/logs.txt', level=logging.DEBUG, format=FORMAT)
logging.debug('Begin Logging')
logging.info('Getting ready to login to Discord...')


@Client.event  # On Bot Startup, Will send some details about the bot and sets it's activity and status. Feel free to remove the print messages, but keep everything else.
async def on_ready():
    if config['Database_Type'].lower() == 'local':
        print("Connecting to KumosLab/Database/Local/userbase.sqlite")
        db = sqlite3.connect('KumosLab/Database/Local/userbase.sqlite')
        cursor = db.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS levelling(
                            user_id INTEGER,
                            name TEXT,
                            guild_id TEXT,
                            level INTEGER,
                            xp INTEGER,
                            background TEXT,
                            xp_colour TEXT,
                            blur INTEGER,
                            border TEXT
                            )""")
        cursor.close()
        print("Connecting to KumosLab/Database/Local/serverbase.sqlite")
        db = sqlite3.connect('KumosLab/Database/Local/serverbase.sqlite')
        cursor = db.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS levelling(
                            guild_id TEXT,
                            admin_role TEXT,
                            main_channel TEXT,
                            talkchannels TEXT)""")
        cursor.close()
        print("Connecting to KumosLab/Database/Local/roles.sqlite")
        db = sqlite3.connect('KumosLab/Database/Local/roles.sqlite')
        cursor = db.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS levelling(
                            guild_id TEXT,
                            role TEXT,
                            role_levels INTEGER
                            )""")
        cursor.close()
    logging.info('Getting Bot Activity from Config')

    ascii_banner = pyfiglet.figlet_format("MODERN LEVELS")
    print(ascii_banner)

    print("Thank you for downloading Modern Levels 2.0 <3 \nIf you run into any issues, want to suggest a feature or "
          "want "
          "a place to hang out, join the Discord! discord.gg/E56eZdNjK4\n")
    print('Logged In As:')
    print(f"Username: {Client.user.name}\nID: {Client.user.id}")
    print(f'Database Type: {str(config["Database_Type"]).title()}')

@Client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    if isinstance(error, RoleNotFound):
        embed = discord.Embed(
            description=f"🔴 **ERROR**: `Role not found! - {config['Prefix']}role <add|remove> <role> <role level>`")
        await ctx.send(embed=embed)
        return
    if isinstance(error, MemberNotFound):
        embed = discord.Embed(
            description=f"🔴 **ERROR**: `Member not found!`")
        await ctx.send(embed=embed)
        return
    raise error

@Client.ipc.route()
async def get_guild_ids(data):
    guildArray = []
    for guild in Client.guilds:
        guildArray.append(guild.id)
    return guildArray

logging.info("------------- Loading -------------")
for fn in listdir("Commands"):
    if fn.endswith(".py"):
        logging.info(f"Loading: {fn}")
        Client.load_extension(f"Commands.{fn[:-3]}")
        logging.info(f"Loaded {fn}")

for fn in listdir("Addons"):
    if fn.endswith(".py"):
        logging.info(f"Loading: {fn} Addon")
        Client.load_extension(f"Addons.{fn[:-3]}")
        logging.info(f"Loaded {fn} Addon")

for fn in listdir("System"):
    if fn.endswith(".py"):
        logging.info(f"Loading: {fn} System")
        Client.load_extension(f"System.{fn[:-3]}")
        logging.info(f"Loaded {fn} System")
logging.info("------------- Finished Loading -------------")

# Uses the bot token to login, so don't remove this.
token = os.getenv("DISCORD_TOKEN")
Client.ipc.start()
Client.run(token)


# End Of Main