import os
import sqlite3

import discord
from pymongo import MongoClient
from ruamel import yaml

with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)


if config['Database_Type'].lower() == 'mongodb':
    MONGODB_URI = os.environ['MONGODB_URI']
    COLLECTION = os.getenv("COLLECTION")
    DB_NAME = os.getenv("DATABASE_NAME")
    cluster = MongoClient(MONGODB_URI)
    levelling = cluster[COLLECTION][DB_NAME]

async def xp(user: discord.Member = None, guild: discord.Guild = None, amount=None):
    if user is None:
        print("Error in 'KumosLab/Database/remove.py' - User is None for 'xp'")
        return
    if guild is None:
        print("Error in 'KumosLab/Database/remove.py' - Guild is None for 'xp'")
        return
    if amount is None:
        print("Error in 'KumosLab/Database/remove.py' - Amount is None for 'xp'")
        return
    try:
        if config['Database_Type'].lower() == "mongodb":
            user_search = levelling.find_one({'user_id': user.id, 'guild_id': guild.id})
            if user_search is None:
                print("User Not Found!")
                return
            # add xp
            levelling.update_one({'user_id': user.id, 'guild_id': guild.id}, {'$inc': {'xp': - amount}})
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
            cursor.execute("UPDATE levelling SET xp = xp - ? WHERE user_id = ? AND guild_id = ?", (amount, user.id, guild.id))
            db.commit()
            cursor.close()
            return
    except Exception as e:
        print("Error in 'KumosLab/Database/remove.py' - " + str(e))
        return

async def level(user: discord.Member = None, guild: discord.Guild = None, amount=None):
    if user is None:
        print("Error in 'KumosLab/Database/remove.py' - User is None for 'level'")
        return
    if guild is None:
        print("Error in 'KumosLab/Database/remove.py' - Guild is None for 'level'")
        return
    if amount is None:
        print("Error in 'KumosLab/Database/remove.py' - Amount is None for 'level'")
        return
    try:
        if config['Database_Type'].lower() == "mongodb":
            member = levelling.find_one({'user_id': user.id, 'guild': guild.id})
            if member is None:
                print("User Not Found!")
                return
            # add level
            levelling.update_one({'user_id': user.id, 'guild_id': guild.id}, {'$inc': {'level': - amount}})
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
            cursor.execute("UPDATE levelling SET level = level - ? WHERE user_id = ? AND guild_id = ?", (amount, user.id, guild.id))
            db.commit()
            cursor.close()
            return
    except Exception as e:
        print("Error in 'KumosLab/Database/remove.py' - " + str(e))
        return

async def role(guild: discord.Guild = None, role_name: discord.Role = None, role_level: int = None):
    if guild is None:
        print("Error in 'KumosLab/Database/remove.py' - Guild is None for 'role'")
        return
    if role is None:
        print("Error in 'KumosLab/Database/remove.py' - Role is None for 'role'")
        return
    if role_level is None:
        print("Error in 'KumosLab/Database/remove.py' - Role_Level is None for 'role'")
        return
    try:
        if config['Database_Type'].lower() == "mongodb":
            # add role
            levelling.update_one({'guild': guild.id}, {'$pull': {'roles': role_name.name, 'role_levels': int(role_level)}})
            return
        elif config['Database_Type'].lower() == "local":
            db = sqlite3.connect("KumosLab/Database/Local/roles.sqlite")
            cursor = db.cursor()
            # delete guild, role and level
            cursor.execute("DELETE FROM levelling WHERE guild_id = ? AND role = ? AND role_levels = ?", (guild.id, role_name.name, role_level))
            db.commit()
            cursor.close()
            return
    except Exception as e:
        print("Error in 'KumosLab/Database/remove.py' - " + str(e))
        return

async def talkchannel(guild: discord.Guild = None, channel: discord.TextChannel = None):
    if guild is None:
        print("Error in 'KumosLab/Database/add.py' - Guild is None for 'talkchannel'")
        return
    if channel is None:
        print("Error in 'KumosLab/Database/add.py' - channel is None for 'talkchannel'")
        return
    try:
        if config['Database_Type'].lower() == "mongodb":
            # find if role is already in database
            talk_db = levelling.find_one({'guild': guild.id, 'talkchannels': channel.id})
            if talk_db is None:
                return "error"
            levelling.update_one({'guild': guild.id}, {'$pull': {'talkchannels': channel.id}})
            return
        elif config['Database_Type'].lower() == "local":
            db = sqlite3.connect("KumosLab/Database/Local/serverbase.sqlite")
            cursor = db.cursor()
            # set talkchannels to none
            cursor.execute("UPDATE levelling SET talkchannels = ? WHERE guild_id = ?", (None, guild.id))
            db.commit()
            cursor.close()
            return
    except Exception as e:
        print("Error in 'KumosLab/Database/remove.py' - " + str(e))
        return








