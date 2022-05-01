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

async def userField(member: discord.Member, guild: discord.Guild):
    db_type = config["Database_Type"]
    if db_type.lower() == "mongodb":
        levelling.insert_one(
            {"guild_id": guild.id, "user_id": member.id, "name": str(member), "level": 1, "xp": 0,
             "background": config['Default_Background'], "xp_colour": config['Default_XP_Colour'], "blur": 0,
             "border": config['Default_Border']})
    elif db_type.lower() == "local":
        db = sqlite3.connect("KumosLab/Database/Local/userbase.sqlite")
        cursor = db.cursor()
        sql = "INSERT INTO levelling (guild_id, user_id, name, level, xp, background, xp_colour, blur, border) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        val = (
        member.guild.id, member.id, str(member), 1, 0, config['Default_Background'], config['Default_XP_Colour'], 0,
        config['Default_Border'])
        cursor.execute(sql, val)
        db.commit()
        cursor.close()