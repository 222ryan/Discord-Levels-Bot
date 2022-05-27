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
        print("Error in 'KumosLab/Database/set.py' - User is None for 'xp'")
        return
    if guild is None:
        print("Error in 'KumosLab/Database/set.py' - Guild is None for 'xp'")
        return
    if amount is None:
        print("Error in 'KumosLab/Database/set.py' - Amount is None for 'xp'")
        return
    try:
        if config['Database_Type'].lower() == "mongodb":
            member = levelling.find_one({'user_id': user.id, 'guild_id': guild.id})
            if member is None:
                print("User Not Found!")
                return
            # add xp
            levelling.update_one({'user_id': user.id, 'guild_id': guild.id}, {'$set': {'xp': amount}})
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
            cursor.execute("UPDATE levelling SET xp = ? WHERE user_id = ? AND guild_id = ?", (amount, user.id, guild.id))
            db.commit()
            cursor.close()
            return
    except Exception as e:
        print("Error in 'KumosLab/Database/add.py' - " + str(e))
        return

async def level(user: discord.Member = None, guild: discord.Guild = None, amount=None):
    if user is None:
        print("Error in 'KumosLab/Database/set.py' - User is None for 'level'")
        return
    if guild is None:
        print("Error in 'KumosLab/Database/set.py' - Guild is None for 'level'")
        return
    if amount is None:
        print("Error in 'KumosLab/Database/set.py' - Amount is None for 'level'")
        return
    try:
        if config['Database_Type'].lower() == "mongodb":
            member = levelling.find_one({'user_id': user.id, 'guild_id': guild.id})
            if member is None:
                print("User Not Found!")
                return
            # add level
            levelling.update_one({'user_id': user.id, 'guild_id': guild.id}, {'$set': {'level': amount}})
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
            cursor.execute("UPDATE levelling SET level = ? WHERE user_id = ? AND guild_id = ?", (amount, user.id, guild.id))
            db.commit()
            cursor.close()
            return
    except Exception as e:
        print("Error in 'KumosLab/Database/set.py' - " + str(e))
        return

async def background(user: discord.Member = None, guild: discord.Guild = None, link=None):
    if user is None:
        print("Error in 'KumosLab/Database/set.py' - User is None for 'background'")
        return
    if guild is None:
        print("Error in 'KumosLab/Database/set.py' - Guild is None for 'background'")
        return
    if link is None:
        print("Error in 'KumosLab/Database/set.py' - Link is None for 'background'")
        return
    try:
        if config['Database_Type'].lower() == "mongodb":
            member = levelling.find_one({'user_id': user.id, 'guild_id': guild.id})
            if member is None:
                print("User Not Found!")
                return
            # add background
            levelling.update_one({'user_id': user.id, 'guild_id': guild.id}, {'$set': {'background': link}})
            return
        elif config['Database_Type'].lower() == "local":
            db = sqlite3.connect("KumosLab/Database/Local/userbase.sqlite")
            cursor = db.cursor()
            cursor.execute("SELECT background FROM levelling WHERE user_id = ? AND guild_id = ?", (user.id, guild.id))
            result = cursor.fetchone()
            if result is None:
                print("User Not Found!")
                return
            # add level
            cursor.execute("UPDATE levelling SET background = ? WHERE user_id = ? AND guild_id = ?", (link, user.id, guild.id))
            db.commit()
            cursor.close()
            return
    except Exception as e:
        print("Error in 'KumosLab/Database/set.py' - " + str(e))
        return

async def border(user: discord.Member = None, guild: discord.Guild = None, link=None):
    if user is None:
        print("Error in 'KumosLab/Database/set.py' - User is None for 'border'")
        return
    if guild is None:
        print("Error in 'KumosLab/Database/set.py' - Guild is None for 'border'")
        return
    if link is None:
        print("Error in 'KumosLab/Database/set.py' - Link is None for 'border'")
        return
    try:
        if config['Database_Type'].lower() == "mongodb":
            member = levelling.find_one({'user_id': user.id, 'guild_id': guild.id})
            if member is None:
                print("User Not Found!")
                return
            # add border
            levelling.update_one({'user_id': user.id, 'guild_id': guild.id}, {'$set': {'border': link}})
            return
        elif config['Database_Type'].lower() == "local":
            db = sqlite3.connect("KumosLab/Database/Local/userbase.sqlite")
            cursor = db.cursor()
            cursor.execute("SELECT border FROM levelling WHERE user_id = ? AND guild_id = ?", (user.id, guild.id))
            result = cursor.fetchone()
            if result is None:
                print("User Not Found!")
                return
            # add level
            cursor.execute("UPDATE levelling SET border = ? WHERE user_id = ? AND guild_id = ?", (link, user.id, guild.id))
            db.commit()
            cursor.close()
            return
    except Exception as e:
        print("Error in 'KumosLab/Database/set.py' - " + str(e))
        return

async def colour(user: discord.Member = None, guild: discord.Guild = None, hex=None):
    if user is None:
        print("Error in 'KumosLab/Database/set.py' - User is None for 'colour'")
        return
    if guild is None:
        print("Error in 'KumosLab/Database/set.py' - Guild is None for 'colour'")
        return
    if hex is None:
        print("Error in 'KumosLab/Database/set.py' - Hex is None for 'colour'")
        return
    try:
        if config['Database_Type'].lower() == "mongodb":
            member = levelling.find_one({'user_id': user.id, 'guild_id': guild.id})
            if member is None:
                print("User Not Found!")
                return
            # add background
            levelling.update_one({'user_id': user.id, 'guild_id': guild.id}, {'$set': {'xp_colour': hex}})
            return
        elif config['Database_Type'].lower() == "local":
            db = sqlite3.connect("KumosLab/Database/Local/userbase.sqlite")
            cursor = db.cursor()
            cursor.execute("SELECT xp_colour FROM levelling WHERE user_id = ? AND guild_id = ?", (user.id, guild.id))
            result = cursor.fetchone()
            if result is None:
                print("User Not Found!")
                return
            # add level
            cursor.execute("UPDATE levelling SET xp_colour = ? WHERE user_id = ? AND guild_id = ?", (hex, user.id, guild.id))
            db.commit()
            cursor.close()
            return
    except Exception as e:
        print("Error in 'KumosLab/Database/set.py' - " + str(e))
        return

async def blur(user: discord.Member = None, guild: discord.Guild = None, amount=None):
    if user is None:
        print("Error in 'KumosLab/Database/set.py' - User is None for 'blur'")
        return
    if guild is None:
        print("Error in 'KumosLab/Database/set.py' - Guild is None for 'blur'")
        return
    if amount is None:
        print("Error in 'KumosLab/Database/set.py' - Amount is None for 'blur'")
        return
    try:
        if config['Database_Type'].lower() == "mongodb":
            member = levelling.find_one({'user_id': user.id, 'guild_id': guild.id})
            if member is None:
                print("User Not Found!")
                return
            # add background
            levelling.update_one({'user_id': user.id, 'guild_id': guild.id}, {'$set': {'blur': amount}})
            return
        elif config['Database_Type'].lower() == "local":
            db = sqlite3.connect("KumosLab/Database/Local/userbase.sqlite")
            cursor = db.cursor()
            cursor.execute("SELECT blur FROM levelling WHERE user_id = ? AND guild_id = ?", (user.id, guild.id))
            result = cursor.fetchone()
            if result is None:
                print("User Not Found!")
                return
            # add level
            cursor.execute("UPDATE levelling SET blur = ? WHERE user_id = ? AND guild_id = ?", (amount, user.id, guild.id))
            db.commit()
            cursor.close()
            return
    except Exception as e:
        print("Error in 'KumosLab/Database/set.py' - " + str(e))
        return

async def mainChannel(guild: discord.Guild = None, channel: discord.TextChannel = None):
    if guild is None:
        print("Error in 'KumosLab/Database/set.py' - Guild is None for 'mainChannel'")
        return
    if channel is None:
        print("Error in 'KumosLab/Database/set.py' - Channel is None for 'mainChannel'")
        return
    try:
        if config['Database_Type'].lower() == "mongodb":
            levelling.update_one({'guild': guild.id}, {'$set': {'main_channel': channel.name}})
            return
        elif config['Database_Type'].lower() == "local":
            db = sqlite3.connect("KumosLab/Database/Local/serverbase.sqlite")
            cursor = db.cursor()
            cursor.execute("UPDATE levelling SET main_channel = ? WHERE guild_id = ?", (channel.name, guild.id))
            db.commit()
            cursor.close()
            return
    except Exception as e:
        print("Error in 'KumosLab/Database/set.py' - " + str(e))
        return





