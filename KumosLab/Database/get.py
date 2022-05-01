import os
import sqlite3
import urllib.request
import json

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

async def xp(user: discord.Member = None, guild: discord.Guild = None):
    if user is None:
        print("Error in 'KumosLab/Database/get.py' - User is None for 'xp'")
        return
    if guild is None:
        print("Error in 'KumosLab/Database/get.py' - Guild is None for 'xp'")
        return
    try:
        if config['Database_Type'].lower() == "mongodb":
            member = levelling.find_one({'user_id': user.id, 'guild_id': guild.id})
            if user is None:
                return "User Not Found!"
            return member['xp']
        elif config['Database_Type'].lower() == "local":
            db = sqlite3.connect("KumosLab/Database/Local/userbase.sqlite")
            cursor = db.cursor()
            cursor.execute("SELECT xp FROM levelling WHERE user_id = ? AND guild_id = ?", (user.id, guild.id))
            result = cursor.fetchone()
            if result is None:
                return "User Not Found!"
            cursor.close()
            return result[0]

    except Exception as e:
        print("Error in 'KumosLab/Database/get.py' - " + str(e))
        return

async def background(user: discord.Member = None, guild: discord.Guild = None):
    if user is None:
        print("Error in 'KumosLab/Database/get.py' - User is None for 'background'")
        return
    if guild is None:
        print("Error in 'KumosLab/Database/get.py' - Guild is None for 'background'")
        return
    try:
        if config['Database_Type'].lower() == "mongodb":
            member = levelling.find_one({'user_id': user.id, 'guild_id': guild.id})
            if member is None:
                print("User Not Found!")
                return
            return member['background']
        elif config['Database_Type'].lower() == "local":
            db = sqlite3.connect("KumosLab/Database/Local/userbase.sqlite")
            cursor = db.cursor()
            cursor.execute("SELECT background FROM levelling WHERE user_id = ? AND guild_id = ?", (user.id, guild.id))
            result = cursor.fetchone()
            if result is None:
                print("User Not Found!")
                return
            cursor.close()
            return result[0]
    except Exception as e:
        print("Error in 'KumosLab/Database/get.py' - " + str(e))
        return

async def border(user: discord.Member = None, guild: discord.Guild = None):
    if user is None:
        print("Error in 'KumosLab/Database/get.py' - User is None for 'border'")
        return
    if guild is None:
        print("Error in 'KumosLab/Database/get.py' - Guild is None for 'border'")
        return
    try:
        if config['Database_Type'].lower() == "mongodb":
            member = levelling.find_one({'user_id': user.id, 'guild_id': guild.id})
            if member is None:
                print("User Not Found!")
                return
            return member['border']
        elif config['Database_Type'].lower() == "local":
            db = sqlite3.connect("KumosLab/Database/Local/userbase.sqlite")
            cursor = db.cursor()
            cursor.execute("SELECT border FROM levelling WHERE user_id = ? AND guild_id = ?", (user.id, guild.id))
            result = cursor.fetchone()
            if result is None:
                print("User Not Found!")
                return
            cursor.close()
            return result[0]
    except Exception as e:
        print("Error in 'KumosLab/Database/get.py' - " + str(e))
        return

async def colour(user: discord.Member = None, guild: discord.Guild = None):
    if user is None:
        print("Error in 'KumosLab/Database/get.py' - User is None for 'background'")
        return
    if guild is None:
        print("Error in 'KumosLab/Database/get.py' - Guild is None for 'background'")
        return
    try:
        if config['Database_Type'].lower() == "mongodb":
            member = levelling.find_one({'user_id': user.id, 'guild_id': guild.id})
            if member is None:
                print("User Not Found!")
                return
            return member['xp_colour']
        elif config['Database_Type'].lower() == "local":
            db = sqlite3.connect("KumosLab/Database/Local/userbase.sqlite")
            cursor = db.cursor()
            cursor.execute("SELECT xp_colour FROM levelling WHERE user_id = ? AND guild_id = ?", (user.id, guild.id))
            result = cursor.fetchone()
            if result is None:
                print("User Not Found!")
                return
            cursor.close()
            return result[0]
    except Exception as e:
        print("Error in 'KumosLab/Database/get.py' - " + str(e))
        return

async def blur(user: discord.Member = None, guild: discord.Guild = None):
    if user is None:
        print("Error in 'KumosLab/Database/get.py' - User is None for 'blur'")
        return
    if guild is None:
        print("Error in 'KumosLab/Database/get.py' - Guild is None for 'blur'")
        return
    try:
        if config['Database_Type'].lower() == "mongodb":
            member = levelling.find_one({'user_id': user.id, 'guild_id': guild.id})
            if member is None:
                print("User Not Found!")
                return
            return member['blur']
        elif config['Database_Type'].lower() == "local":
            db = sqlite3.connect("KumosLab/Database/Local/userbase.sqlite")
            cursor = db.cursor()
            cursor.execute("SELECT blur FROM levelling WHERE user_id = ? AND guild_id = ?", (user.id, guild.id))
            result = cursor.fetchone()
            if result is None:
                print("User Not Found!")
                return
            cursor.close()
            return result[0]
    except Exception as e:
        print("Error in 'KumosLab/Database/get.py' - " + str(e))
        return


async def level(user: discord.Member = None, guild: discord.Guild = None):
    if user is None:
        print("Error in 'KumosLab/Database/get.py' - User is None for 'level'")
        return
    if guild is None:
        print("Error in 'KumosLab/Database/get.py' - Guild is None for 'level'")
        return
    try:
        if config['Database_Type'].lower() == "mongodb":
            member = levelling.find_one({'user_id': user.id, 'guild_id': guild.id})
            if member is None:
                print("User Not Found!")
                return
            return member['level']
        elif config['Database_Type'].lower() == "local":
            db = sqlite3.connect("KumosLab/Database/Local/userbase.sqlite")
            cursor = db.cursor()
            cursor.execute("SELECT level FROM levelling WHERE user_id = ? AND guild_id = ?", (user.id, guild.id))
            result = cursor.fetchone()
            if result is None:
                print("User Not Found!")
                return
            cursor.close()
            return result[0]
    except Exception as e:
        print("Error in 'KumosLab/Database/get.py' - " + str(e))
        return

async def rankings(user: discord.Member = None, guild: discord.Guild = None):
    if guild is None:
        print("Error in 'KumosLab/Database/get.py' - Guild is None for 'rankings'")
        return
    try:
        if config['Database_Type'].lower() == "mongodb":
            stats = levelling.find_one({"guild_id": guild.id, "user_id": user.id})
            rankings = levelling.find({"guild_id": guild.id}).sort("xp", -1)
            rank = 0
            for x in rankings:
                rank += 1
                if stats["user_id"] == x["user_id"]:
                    break
            return rank
        elif config['Database_Type'].lower() == "local":
            db = sqlite3.connect("KumosLab/Database/Local/userbase.sqlite")
            cursor = db.cursor()
            rankings = cursor.execute("SELECT * FROM levelling WHERE guild_id = ? ORDER BY xp DESC", (guild.id,))
            rank = 0
            for x in rankings:
                rank += 1
                if user.id == x[0]:
                    break
            cursor.close()
            return rank
    except Exception as e:
        print("Error in 'KumosLab/Database/get.py' - " + str(e))
        return

async def mainChannel(guild: discord.Guild = None):
    if guild is None:
        print("Error in 'KumosLab/Database/get.py' - Guild is None for 'mainChannel'")
        return
    try:
        if config['Database_Type'].lower() == "mongodb":
            server = levelling.find_one({"guild": guild.id})
            if server is None:
                print("Server Not Found!")
                return
            return server["main_channel"]
        elif config['Database_Type'].lower() == "local":
            db = sqlite3.connect("KumosLab/Database/Local/serverbase.sqlite")
            cursor = db.cursor()
            cursor.execute("SELECT main_channel FROM levelling WHERE guild_id = ?", (guild.id,))
            result = cursor.fetchone()
            if result is None:
                print("Server Not Found!")
                return
            cursor.close()
            return result[0]
    except Exception as e:
        print("Error in 'KumosLab/Database/get.py' - " + str(e))
        return

async def roles(guild: discord.Guild = None):
    if guild is None:
        print("Error in 'KumosLab/Database/get.py' - Guild is None for 'roles'")
        return
    try:
        if config['Database_Type'].lower() == "mongodb":
            server = levelling.find_one({"guild": guild.id})
            if server is None:
                print("Server Not Found!")
                return
            return server["roles"]
        elif config['Database_Type'].lower() == "local":
            db = sqlite3.connect("KumosLab/Database/Local/roles.sqlite")
            cursor = db.cursor()
            # get all roles
            cursor.execute("SELECT role FROM levelling WHERE guild_id = ?", (guild.id,))
            result = cursor.fetchall()
            if result is None:
                print("Server Not Found!")
                return
            cursor.close()
            return result
    except Exception as e:
        print("Error in 'KumosLab/Database/get.py' - " + str(e))
        return

async def roleLevel(guild: discord.Guild = None):
    if guild is None:
        print("Error in 'KumosLab/Database/get.py' - Guild is None for 'roleLevel'")
        return
    try:
        if config['Database_Type'].lower() == "mongodb":
            server = levelling.find_one({"guild": guild.id})
            if server is None:
                print("Server Not Found!")
                return
            return server["role_levels"]
        elif config['Database_Type'].lower() == "local":
            db = sqlite3.connect("KumosLab/Database/Local/roles.sqlite")
            cursor = db.cursor()
            cursor.execute("SELECT role_levels FROM levelling WHERE guild_id = ?", (guild.id,))
            result = cursor.fetchall()
            if result is None:
                print("Server Not Found!")
                return
            cursor.close()
            # convert to an int array
            return [int(x[0]) for x in result]

    except Exception as e:
        print("Error in 'KumosLab/Database/get.py' - " + str(e))
        return

async def talkchannels(guild: discord.Guild = None):
    if guild is None:
        print("Error in 'KumosLab/Database/get.py' - Guild is None for 'talkchannels'")
        return
    try:
        if config['Database_Type'].lower() == "mongodb":
            server = levelling.find_one({"guild": guild.id})
            if server is None:
                print("Server Not Found!")
                return
            return server["talkchannels"]
        elif config['Database_Type'].lower() == "local":
            db = sqlite3.connect("KumosLab/Database/Local/serverbase.sqlite")
            cursor = db.cursor()
            cursor.execute("SELECT talkchannels FROM levelling WHERE guild_id = ?", (guild.id,))
            result = cursor.fetchall()
            if result is None:
                print("Server Not Found!")
                return
            cursor.close()
            # convert to an int array
            return [x[0] for x in result]

    except Exception as e:
        print("Error in 'KumosLab/Database/get.py' - " + str(e))
        return

async def clan(guild: discord.Guild = None, clan_Name: str = None):
    if guild is None:
        print("Error in 'KumosLab/Database/get.py' - Guild is None for 'clan'")
        return
    if clan_Name is None:
        print("Error in 'KumosLab/Database/get.py' - Clan Name is None for 'clan'")
        return
    try:
        if config['Database_Type'].lower() == "mongodb":
            server = levelling.find_one({"clans_guild": guild.id, "clan_name": clan_Name})
            if server is None:
                return "error"
            return server["clan_name"]
        elif config['Database_Type'].lower() == "local":
            db = sqlite3.connect("KumosLab/Database/Local/clans.sqlite")
            cursor = db.cursor()
            cursor.execute("SELECT clan_Name FROM levelling WHERE clans_guild = ? AND clan_name = ?", (guild.id, clan_Name))
            result = cursor.fetchone()
            if result is None:
                return "error"
            cursor.close()
            return result[0]

    except Exception as e:
        print("Error in 'KumosLab/Database/get.py' - " + str(e))
        return

async def clanXP(guild: discord.Guild = None, clan_Name: str = None):
    if guild is None:
        print("Error in 'KumosLab/Database/get.py' - Guild is None for 'clanXP'")
        return
    if clan_Name is None:
        print("Error in 'KumosLab/Database/get.py' - Clan Name is None for 'clanXP'")
        return
    try:
        if config['Database_Type'].lower() == "mongodb":
            server = levelling.find_one({"clans_guild": guild.id, "clan_name": clan_Name})
            if server is None:
                return "error"
            return server["xp"]
        elif config['Database_Type'].lower() == "local":
            db = sqlite3.connect("KumosLab/Database/Local/clans.sqlite")
            cursor = db.cursor()
            cursor.execute("SELECT xp FROM levelling WHERE clans_guild = ? AND clan_name = ?", (guild.id, clan_Name))
            result = cursor.fetchone()
            if result is None:
                return "error"
            cursor.close()
            return result[0]

    except Exception as e:
        print("Error in 'KumosLab/Database/get.py' - " + str(e))
        return

async def clanOwner(guild: discord.Guild = None, clan_Name: str = None):
    if guild is None:
        print("Error in 'KumosLab/Database/get.py' - Guild is None for 'clanXP'")
        return
    if clan_Name is None:
        print("Error in 'KumosLab/Database/get.py' - Clan Name is None for 'clanXP'")
        return
    try:
        if config['Database_Type'].lower() == "mongodb":
            server = levelling.find_one({"clans_guild": guild.id, "clan_name": clan_Name})
            if server is None:
                return "error"
            return server["owner"]
        elif config['Database_Type'].lower() == "local":
            db = sqlite3.connect("KumosLab/Database/Local/clans.sqlite")
            cursor = db.cursor()
            cursor.execute("SELECT owner FROM levelling WHERE clans_guild = ? AND clan_name = ?", (guild.id, clan_Name))
            result = cursor.fetchone()
            if result is None:
                return "error"
            cursor.close()
            client = discord.Client()
            return client.get_user(result[0])

    except Exception as e:
        print("Error in 'KumosLab/Database/get.py' - " + str(e))
        return

async def clanLevel(guild: discord.Guild = None, clan_Name: str = None):
    if guild is None:
        print("Error in 'KumosLab/Database/get.py' - Guild is None for 'clanXP'")
        return
    if clan_Name is None:
        print("Error in 'KumosLab/Database/get.py' - Clan Name is None for 'clanXP'")
        return
    try:
        if config['Database_Type'].lower() == "mongodb":
            server = levelling.find_one({"clans_guild": guild.id, "clan_name": clan_Name})
            if server is None:
                return "error"
            return server["level"]
        elif config['Database_Type'].lower() == "local":
            db = sqlite3.connect("KumosLab/Database/Local/clans.sqlite")
            cursor = db.cursor()
            cursor.execute("SELECT level FROM levelling WHERE clans_guild = ? AND clan_name = ?", (guild.id, clan_Name))
            result = cursor.fetchone()
            if result is None:
                return "error"
            cursor.close()
            return result[0]

    except Exception as e:
        print("Error in 'KumosLab/Database/get.py' - " + str(e))
        return

async def clanLogo(guild: discord.Guild = None, clan_Name: str = None):
    if guild is None:
        print("Error in 'KumosLab/Database/get.py' - Guild is None for 'clanXP'")
        return
    if clan_Name is None:
        print("Error in 'KumosLab/Database/get.py' - Clan Name is None for 'clanXP'")
        return
    try:
        if config['Database_Type'].lower() == "mongodb":
            server = levelling.find_one({"clans_guild": guild.id, "clan_name": clan_Name})
            if server is None:
                return "error"
            return server["logo"]
        elif config['Database_Type'].lower() == "local":
            db = sqlite3.connect("KumosLab/Database/Local/clans.sqlite")
            cursor = db.cursor()
            cursor.execute("SELECT logo FROM levelling WHERE clans_guild = ? AND clan_name = ?", (guild.id, clan_Name))
            result = cursor.fetchone()
            if result is None:
                return "error"
            cursor.close()
            return result[0]

    except Exception as e:
        print("Error in 'KumosLab/Database/get.py' - " + str(e))
        return

async def clanColour(guild: discord.Guild = None, clan_Name: str = None):
    if guild is None:
        print("Error in 'KumosLab/Database/get.py' - Guild is None for 'clanXP'")
        return
    if clan_Name is None:
        print("Error in 'KumosLab/Database/get.py' - Clan Name is None for 'clanXP'")
        return
    try:
        if config['Database_Type'].lower() == "mongodb":
            server = levelling.find_one({"clans_guild": guild.id, "clan_name": clan_Name})
            if server is None:
                return "error"
            return server["colour"]
        elif config['Database_Type'].lower() == "local":
            db = sqlite3.connect("KumosLab/Database/Local/clans.sqlite")
            cursor = db.cursor()
            cursor.execute("SELECT colour FROM levelling WHERE clans_guild = ? AND clan_name = ?", (guild.id, clan_Name))
            result = cursor.fetchone()
            if result is None:
                return "error"
            cursor.close()
            return result[0]

    except Exception as e:
        print("Error in 'KumosLab/Database/get.py' - " + str(e))
        return

async def clanMembers(guild: discord.Guild = None, clan_Name: str = None):
    if guild is None:
        print("Error in 'KumosLab/Database/get.py' - Guild is None for 'clanXP'")
        return
    if clan_Name is None:
        print("Error in 'KumosLab/Database/get.py' - Clan Name is None for 'clanXP'")
        return
    try:
        if config['Database_Type'].lower() == "mongodb":
            server = levelling.find_one({"clans_guild": guild.id, "clan_name": clan_Name})
            if server is None:
                return "error"
            return server["members"]
        elif config['Database_Type'].lower() == "local":
            db = sqlite3.connect("KumosLab/Database/Local/clans.sqlite")
            cursor = db.cursor()
            cursor.execute("SELECT members FROM levelling WHERE clans_guild = ? AND clan_name = ?", (guild.id, clan_Name))
            result = cursor.fetchone()
            if result is None:
                return "error"
            cursor.close()
            return result[0]

    except Exception as e:
        print("Error in 'KumosLab/Database/get.py' - " + str(e))
        return

async def latestVersion():
    with urllib.request.urlopen("https://api.github.com/repos/KumosLab/Discord-Levels-Bot/releases/latest") as url:
        data = json.loads(url.read().decode())
        return data["tag_name"]





