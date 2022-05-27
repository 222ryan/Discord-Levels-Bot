# Imports
import random

from discord.ext import commands
from pymongo import MongoClient
from ruamel.yaml import YAML
import os
from dotenv import load_dotenv
import sqlite3

import KumosLab.Database.get
import KumosLab.Database.set
import KumosLab.Database.add
import KumosLab.Database.check
import KumosLab.Database.insert

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


class levelsys(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if not ctx.author.bot:
            if ctx.content.startswith(config["Prefix"]):
                return

            if config['loader_type'].lower() == 'message':
                user_check = await KumosLab.Database.get.xp(user=ctx.author, guild=ctx.guild)
                if user_check == "User Not Found!":
                    await KumosLab.Database.insert.userField(member=ctx.author, guild=ctx.guild)

            if config['XP_Chance'] is True:
                chance_rate = config['XP_Chance_Rate']
                random_num = random.randint(1, chance_rate)
                if random_num != chance_rate:
                    return

            channels = await KumosLab.Database.get.talkchannels(guild=ctx.guild)
            channel_Array = []
            channel_List = []
            for channel in channels:
                channel_Array.append(channel)
            if len(channel_Array) < 1 or channel_Array[0] is None:
                pass
            else:
                for x in channel_Array:
                    channel = self.client.get_channel(int(x))
                    channel_List.append(channel.name)

            if str(channel_List) == "[]":
                pass
            elif channel_List is not None:
                if ctx.channel.name in channel_List:
                    pass
                else:
                    return

            xp_type = config['xp_type']
            if xp_type.lower() == "normal":
                to_add = config['xp_normal_amount']
                await KumosLab.Database.add.xp(user=ctx.author, guild=ctx.guild, amount=to_add)
            elif xp_type.lower() == "words":
                # get the length of the message
                res = len(ctx.content.split())
                message_length = int(res)
                await KumosLab.Database.add.xp(user=ctx.author, guild=ctx.guild, amount=message_length)
            elif xp_type.lower() == "ranrange":
                # get ranges from config
                min = config['xp_ranrange_min']
                max = config['xp_ranrange_max']
                num = random.randint(min, max)
                await KumosLab.Database.add.xp(user=ctx.author, guild=ctx.guild, amount=num)

            await KumosLab.Database.check.levelUp(user=ctx.author, guild=ctx.guild)

    # on guild join
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        # get database type from config file
        db_type = config["Database_Type"]
        if db_type.lower() == "mongodb":
            levelling.insert_one({"guild": guild.id, "main_channel": None, "admin_role": None, "roles": [],
                                  "role_levels": [], 'talkchannels': []})
            for member in guild.members:
                # check if member is a bot
                if not member.bot:
                    levelling.insert_one(
                        {"guild_id": guild.id, "user_id": member.id, "name": str(member), "level": 1, "xp": 0,
                         "background": config['Default_Background'], "xp_colour": config['Default_XP_Colour'],
                         "blur": 0, "border": config['Default_Border']})
        elif db_type.lower() == "local":
            db = sqlite3.connect("KumosLab/Database/Local/serverbase.sqlite")
            cursor = db.cursor()
            sql = "INSERT INTO levelling (guild_id, admin_role, main_channel, talkchannels) VALUES (?, ?, ?, ?)"
            val = (guild.id, None, None, None)
            cursor.execute(sql, val)
            db.commit()
            for member in guild.members:
                # check if member is a bot
                db = sqlite3.connect("KumosLab/Database/Local/userbase.sqlite")
                cursor = db.cursor()
                if not member.bot:
                    sql = "INSERT INTO levelling (guild_id, user_id, name, level, xp, background, xp_colour, blur, border) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
                    val = (
                    guild.id, member.id, str(member), 1, 0, config['Default_Background'], config['Default_XP_Colour'],
                    0, config['Default_Border'])
                    cursor.execute(sql, val)
                    db.commit()
                else:
                    continue
            cursor.close()

    # on guild leave
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        # get database type from config file
        db_type = config["Database_Type"]
        if db_type.lower() == "mongodb":
            levelling.delete_one({"guild": guild.id})
            for member in guild.members:
                levelling.delete_one({"guild_id": guild.id, "user_id": member.id})
        elif db_type.lower() == "local":
            db = sqlite3.connect("KumosLab/Database/Local/serverbase.sqlite")
            cursor = db.cursor()
            sql = "DELETE FROM levelling WHERE guild_id = ?"
            val = (guild.id,)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            for member in guild.members:
                db = sqlite3.connect("KumosLab/Database/Local/userbase.sqlite")
                cursor = db.cursor()
                sql = "DELETE FROM levelling WHERE guild_id = ? AND user_id = ?"
                val = (guild.id, member.id)
                cursor.execute(sql, val)
                db.commit()
            cursor.close()

    # on member join
    @commands.Cog.listener()
    async def on_member_join(self, member):
        await KumosLab.Database.insert.userField(member=member, guild=member.guild)

    # on member leave
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        # get database type from config file
        db_type = config["Database_Type"]
        if db_type.lower() == "mongodb":
            levelling.delete_one({"guild_id": member.guild.id, "user_id": member.id})
        elif db_type.lower() == "local":
            db = sqlite3.connect("KumosLab/Database/Local/userbase.sqlite")
            cursor = db.cursor()
            sql = "DELETE FROM levelling WHERE guild_id = ? AND user_id = ?"
            val = (member.guild.id, member.id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()


def setup(client):
    client.add_cog(levelsys(client))

# End Of Level System
