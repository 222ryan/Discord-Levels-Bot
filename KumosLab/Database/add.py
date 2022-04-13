import os
import sqlite3

import discord
from pymongo import MongoClient
from ruamel import yaml

with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)


# check if clan.py in addon folder
if os.path.isfile("Addons/clan.py"):
    with open("Configs/clan_addon.yml", "r", encoding="utf-8") as file:
        clan_config = yaml.load(file)


if config['Database_Type'].lower() == 'mongodb':
    MONGODB_URI = os.environ['MONGODB_URI']
    COLLECTION = os.getenv("COLLECTION")
    DB_NAME = os.getenv("DATABASE_NAME")
    cluster = MongoClient(MONGODB_URI)
    levelling = cluster[COLLECTION][DB_NAME]

async def xp(user: discord.Member = None, guild: discord.Guild = None, amount=None):
    if user is None:
        print("Error in 'KumosLab/Database/add.py' - User is None for 'xp'")
        return
    if guild is None:
        print("Error in 'KumosLab/Database/add.py' - Guild is None for 'xp'")
        return
    if amount is None:
        print("Error in 'KumosLab/Database/add.py' - Amount is None for 'xp'")
        return
    try:
        if config['Database_Type'].lower() == "mongodb":
            user_find = levelling.find_one({'user_id': user.id, 'guild_id': guild.id})
            if user_find is None:
                print("User Not Found!")
                return
            # add xp
            levelling.update_one({'user_id': user.id, 'guild_id': guild.id}, {'$inc': {'xp': + amount}})
            return
        elif config['Database_Type'].lower() == "local":
            db = sqlite3.connect("KumosLab/Database/Local/userbase.sqlite")
            cursor = db.cursor()
            cursor.execute("SELECT xp FROM levelling WHERE user_id = ? AND guild_id = ?", (user.id, guild.id))
            result = cursor.fetchone()
            if result is None:
                print("User Not Found!")
                return
            # add xp
            cursor.execute("UPDATE levelling SET xp = xp + ? WHERE user_id = ? AND guild_id = ?", (amount, user.id, guild.id))
            db.commit()
            cursor.close()
            return
    except Exception as e:
        print("Error in 'KumosLab/Database/add.py' - " + str(e))
        return

async def level(user: discord.Member = None, guild: discord.Guild = None, amount=None):
    if user is None:
        print("Error in 'KumosLab/Database/add.py' - User is None for 'level'")
        return
    if guild is None:
        print("Error in 'KumosLab/Database/add.py' - Guild is None for 'level'")
        return
    if amount is None:
        print("Error in 'KumosLab/Database/add.py' - Amount is None for 'level'")
        return
    try:
        if config['Database_Type'].lower() == "mongodb":
            member = levelling.find_one({'user_id': user.id, 'guild_id': guild.id})
            if member is None:
                print("User Not Found!")
                return
            # add level
            levelling.update_one({'user_id': user.id, 'guild_id': guild.id}, {'$inc': {'level': + amount}})
            return
        elif config['Database_Type'].lower() == "local":
            db = sqlite3.connect("KumosLab/Database/Local/userbase.sqlite")
            cursor = db.cursor()
            cursor.execute("SELECT level FROM levelling WHERE user_id = ? AND guild_id = ?", (user.id, guild.id))
            result = cursor.fetchone()
            if result is None:
                print("User Not Found!")
                return
            # add level
            cursor.execute("UPDATE levelling SET level = level + ? WHERE user_id = ? AND guild_id = ?", (amount, user.id, guild.id))
            db.commit()
            cursor.close()
            return
    except Exception as e:
        print("Error in 'KumosLab/Database/add.py' - " + str(e))
        return

async def role(guild: discord.Guild = None, role_name: discord.Role = None, role_level: int = None):
    if guild is None:
        print("Error in 'KumosLab/Database/add.py' - Guild is None for 'role'")
        return
    if role is None:
        print("Error in 'KumosLab/Database/add.py' - Role is None for 'role'")
        return
    if role_level is None:
        print("Error in 'KumosLab/Database/add.py' - Role_Level is None for 'role'")
        return
    try:
        if config['Database_Type'].lower() == "mongodb":
            # find if role is already in database
            role_db = levelling.find_one({'guild_id': guild.id, 'role_name': role_name.name})
            if role_db is not None:
                return "error"
            # add role
            levelling.update_one({'guild': guild.id}, {'$push': {'roles': role_name.name, 'role_levels': int(role_level)}})
            return
        elif config['Database_Type'].lower() == "local":
            db = sqlite3.connect("KumosLab/Database/Local/roles.sqlite")
            cursor = db.cursor()
            # find if role is already in database
            cursor.execute("SELECT * FROM levelling WHERE guild_id = ? AND role = ?", (guild.id, role_name.name))
            result = cursor.fetchone()
            if result is not None:
                return "error"
            # insert guild, role and level
            cursor.execute("INSERT INTO levelling (guild_id, role, role_levels) VALUES (?, ?, ?)", (guild.id, role_name.name, role_level))
            db.commit()
            cursor.close()
            return
    except Exception as e:
        print("Error in 'KumosLab/Database/add.py' - " + str(e))
        return

async def talkchannel(guild: discord.Guild = None, channel: discord.TextChannel = None):
    if guild is None:
        print("Error in 'KumosLab/Database/add.py' - Guild is None for 'talkchannel'")
        return
    if channel is None:
        print("Error in 'KumosLab/Database/add.py' - Talk_Channel is None for 'talkchannel'")
        return
    try:
        if config['Database_Type'].lower() == "mongodb":
            talk_db = levelling.find_one({'guild_id': guild.id, 'talkchannels': channel.id})
            if talk_db is not None:
                return "error"
            levelling.update_one({'guild': guild.id}, {'$push': {'talkchannels': channel.id}})
            return
        elif config['Database_Type'].lower() == "local":
            db = sqlite3.connect("KumosLab/Database/Local/serverbase.sqlite")
            cursor = db.cursor()
            cursor.execute("SELECT * FROM levelling WHERE guild_id = ? AND talkchannels = ?", (guild.id, channel.id))
            result = cursor.fetchone()
            if result is not None:
                return "error"
            # update talkchannels to add channel to list
            cursor.execute("UPDATE levelling SET talkchannels = ? WHERE guild_id = ?", (channel.id, guild.id))
            db.commit()
            cursor.close()
            return
    except Exception as e:
        print("Error in 'KumosLab/Database/add.py' - " + str(e))
        return

async def clan(guild: discord.Guild = None, clan_name: str = None, owner: discord.Member = None):
    if guild is None:
        print("Error in 'KumosLab/Database/add.py' - Guild is None for 'clan'")
        return
    if clan_name is None:
        print("Error in 'KumosLab/Database/add.py' - Clan Name is None for 'clan'")
        return
    if owner is None:
        print("Error in 'KumosLab/Database/add.py' - Owner is None for 'clan'")
        return
    try:
        if config['Database_Type'].lower() == "mongodb":
            role_db = levelling.find_one({'clans_guild': guild.id, 'clan_name': clan_name})
            if role_db is not None:
                return "error"
            levelling.insert_one({'clans_guild': guild.id, 'clan_name': clan_name, 'owner': owner.id, 'members': [owner.id], 'level': 1, 'xp': 0, 'logo': clan_config['default_logo'], 'colour': clan_config['default_colour']})
            return
        elif config['Database_Type'].lower() == "local":
            db = sqlite3.connect("KumosLab/Database/Local/clans.sqlite")
            cursor = db.cursor()
            cursor.execute("SELECT * FROM levelling WHERE clans_guild = ? AND clan_name = ?", (guild.id, clan_name))
            result = cursor.fetchone()
            if result is not None:
                return "error"
            cursor.execute("INSERT INTO levelling (clans_guild, clan_name, owner, members, level, xp, logo, colour) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (guild.id, clan_name, str(owner.id), owner.id, 1, 0, clan_config['default_logo'], clan_config['default_colour']))
            db.commit()
            cursor.close()
            return
    except Exception as e:
        print("Error in 'KumosLab/Database/add.py' - " + str(e))
        return







