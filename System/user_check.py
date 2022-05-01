import asyncio
import functools
import os
import sqlite3
import typing

from discord.ext import commands
from dotenv import load_dotenv
from pymongo import MongoClient
from ruamel.yaml import YAML

yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)

# Loads the .env file and gets the required information
load_dotenv()

if config['Database_Type'].lower() == 'mongodb':
    MONGODB_URI = os.environ['MONGODB_URI']
    COLLECTION = os.getenv("COLLECTION")
    DB_NAME = os.getenv("DATABASE_NAME")
    cluster = MongoClient(MONGODB_URI)
    levelling = cluster[COLLECTION][DB_NAME]



class user_check(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def check(self):
        # get database type from config file
        print(f"[User-Check] Checking for users & guilds...")
        db_type = config["Database_Type"]
        if db_type.lower() == "mongodb":
            for member in self.client.get_all_members():
                if not member.bot:
                    if not levelling.find_one({"user_id": member.id, "guild_id": member.guild.id}):
                        levelling.insert_one(
                            {"guild_id": member.guild.id, "user_id": member.id, "name": str(member), "level": 1,
                             "xp": 0,
                             "background": config['Default_Background'], "xp_colour": config['Default_XP_Colour'],
                             "blur": 0, "border": config['Default_Border']})
                        print(f"[User-Check] Added {member.name} to MongoDB Database.")
                    else:
                        continue
            for guild in self.client.guilds:
                if not levelling.find_one({"guild": guild.id}):
                    levelling.insert_one({"guild": guild.id, "main_channel": None, "admin_role": None, "roles": [],
                                          "role_levels": [], 'talkchannels': []})
                    print(f"[User-Check] Added {guild.name} to MongoDB Database.")
                else:
                    continue
        elif db_type.lower() == "local":
            for guild in self.client.guilds:
                db = sqlite3.connect("KumosLab/Database/Local/serverbase.sqlite")
                cursor = db.cursor()
                cursor.execute("SELECT * FROM levelling where guild_id = ?", (guild.id,))
                if cursor.fetchone() is None:
                    sql = "INSERT INTO levelling (guild_id, admin_role, main_channel, talkchannels) VALUES (?, ?, ?, ?) "
                    cursor.execute(sql, (guild.id, None, None, None))
                    print(f"[User-Check] Added {guild.name} to SQLite Database.")
                    db.commit()
                    cursor.close()
                for member in guild.members:
                    # check if member is a bot
                    db = sqlite3.connect("KumosLab/Database/Local/userbase.sqlite")
                    cursor = db.cursor()
                    if not member.bot:
                        cursor.execute("SELECT * FROM levelling WHERE user_id = ? AND guild_id = ?",
                                       (member.id, guild.id))
                        result = cursor.fetchone()
                        if result is None:
                            sql = "INSERT INTO levelling (guild_id, user_id, name, level, xp, background, xp_colour, blur, border) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
                            val = (guild.id, member.id, str(member), 1, 0, config['Default_Background'],
                                   config['Default_XP_Colour'], 0, config['Default_Border'])
                            cursor.execute(sql, val)
                            print(f"[User-Check] Added {member.name} to SQLite Database.")
                            db.commit()
                        else:
                            continue



    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.wait_until_ready()
        if config['loader_type'].lower() == 'startup':
            await user_check.check(self)



def setup(client):
    client.add_cog(user_check(client))
