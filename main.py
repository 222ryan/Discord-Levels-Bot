# Version 2.9.1

# Imports
from discord.ext import commands
from discord.ext.commands import CommandNotFound, MissingRequiredArgument, CommandInvokeError, MissingRole
import discord
from ruamel.yaml import YAML
import logging

# Opens the config and reads it, no need for changes unless you'd like to change the library (no need to do so unless having issues with ruamel)
yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)


# Command Prefix + Removes the default discord.py help command
client = commands.Bot(command_prefix=config['Prefix'], intents=discord.Intents.all(), case_insensitive=True)
client.remove_command('help')

if config['enable_log'] is True:
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='Logs/logs.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)


@client.event  # On Bot Startup, Will send some details about the bot and sets it's activity and status. Feel free to remove the print messages, but keep everything else.
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
    print("Started System: Levels")
    await client.change_presence(status=config_activity, activity=activity)


# If enabled in config, will send a welcome message + adds a role if a new user joins the guild (if roles are enabled).
@client.event
async def on_member_join(member):
    if config['join_leave_message'] is True:
        channel = client.get_channel(config['join_leave_channel'])
        embed = discord.Embed(title=f"**:man_raising_hand: WELCOME**", description=f"Welcome **{member.mention}** to **{member.guild.name}**!", colour=discord.Colour.green())
        embed.set_author(name=member.name, icon_url=member.avatar_url)
        embed.set_thumbnail(url=member.guild.icon_url)
        await channel.send(embed=embed)
        if config['add_role'] is True:
            rank = discord.utils.get(member.guild.roles, name=config['on_join_role'])
            await member.add_roles(rank)
            print(f"User: {member} was given the {rank} role.")


# If enabled in config, will send a leave message if a user leaves the guild
@client.event
async def on_member_remove(member):
    if config['join_leave_message'] is True:
        channel = client.get_channel(config['join_leave_channel'])
        embed = discord.Embed(title=f"**:man_raising_hand: GOODBYE**", description=f"**{member.mention}** has left **{member.guild.name}**!", colour=discord.Colour.red())
        embed.set_author(name=member.name, icon_url=member.avatar_url)
        embed.set_thumbnail(url=member.guild.icon_url)
        await channel.send(embed=embed)


@client.event  # Stops Certain errors from being thrown in the console (Don't remove as it'll cause command error messages to not send! - Only remove if adding features and needed for testing (Don't forget to re-add)!)
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    if isinstance(error, MissingRequiredArgument):
        return
    if isinstance(error, CommandInvokeError):
        return
    if isinstance(error, MissingRole):
        return
    raise error

client.load_extension("Systems.spamsys")
client.load_extension("Systems.levelsys")


# Uses the bot token to login, so don't remove this.
client.run(config['Bot_Token'])

# End Of Main
