import asyncio
import os
import sqlite3

import discord
from discord.ext import commands
from pymongo import MongoClient
from ruamel.yaml import YAML



yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)

if config['Database_Type'].lower() == 'mongodb':
    MONGODB_URI = os.environ['MONGODB_URI']
    COLLECTION = os.getenv("COLLECTION")
    DB_NAME = os.getenv("DATABASE_NAME")
    cluster = MongoClient(MONGODB_URI)
    levelling = cluster[COLLECTION][DB_NAME]

async def leaderboard(self=None, ctx=None, guild=None):
    if self is None:
        print("[Leaderboard-MongoDB] Self is None")
        return
    if ctx is None:
        print("[Leaderboard-MongoDB] Context is None")
        return
    if guild is None:
        print("[Leaderboard-MongoDB] Guild is None")
        return

    result = levelling.find({"guild_id": ctx.guild.id, "xp": {"$exists": True}}).sort(
        "xp", -1)

    if result is None:
        print("Server Not Found!")

    users = []
    level = []
    xp = []

    for x in result:
        users.append(x["name"])
        level.append(x["level"])
        xp.append(x["xp"])

    embed = discord.Embed(title=f":trophy: {guild}'s Leaderboard", colour=config['leaderboard_embed_colour'])

    pagination = list(zip(users, level, xp))
    pages = [pagination[i:i + 10] for i in range(0, len(pagination), 10)]
    page = 0
    num = 0
    user_list = []
    level_list = []
    xp_list = []
    for i in pages:
        embed.clear_fields()
        for users, levels, xp in i:
            num += 1
            embed.add_field(name=f"#{num}: {users}", value=f"```Level: {levels:,} - {xp:,} XP```", inline=False)
        embed.set_footer(text=f"Page {page + 1}/{len(pages)}")
        message = await ctx.send(embed=embed)
        page += 1
        await message.add_reaction("⬅")
        await message.add_reaction("➡")
        await message.add_reaction("❌")

        while True:
            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ["⬅", "➡", "❌"] and reaction.message.id == message.id

            try:
                reaction, user = await ctx.bot.wait_for("reaction_add", timeout=60.0, check=check)

                if str(reaction.emoji) == "⬅":
                    if page == 1:
                        pass
                    else:
                        page -= 1
                        embed.clear_fields()
                        for users, levels, xp in pages[page - 1]:
                            num -= 1
                            user_list.append(users)
                            level_list.append(levels)
                            xp_list.append(xp)
                        for x in range(0, 10):
                            embed.add_field(name=f"#{x + 1 + num - len(user_list)}: {user_list[x]}",
                                            value=f"```Level: {level_list[x]:,} - {xp_list[x]:,} XP```", inline=True)
                        user_list.clear()
                        level_list.clear()
                        xp_list.clear()
                        embed.set_footer(text=f"Page {page}/{len(pages)}")
                        await message.edit(embed=embed)
                        await message.remove_reaction("⬅", user)
                        await message.remove_reaction("➡", user)
                        await message.remove_reaction("❌", user)
                elif str(reaction.emoji) == "➡":
                    if page == len(pages):
                        pass
                    else:
                        page += 1
                        embed.clear_fields()
                        for users, levels, xp in pages[page - 1]:
                            num += 1
                            user_list.append(users)
                            level_list.append(levels)
                            xp_list.append(xp)
                        for x in range(0, 10):
                            embed.add_field(name=f"#{x + 1 + num - len(user_list)}: {user_list[x]}",
                                            value=f"```Level: {level_list[x]:,} - {xp_list[x]:,} XP```", inline=True)
                        user_list.clear()
                        level_list.clear()
                        xp_list.clear()
                        embed.set_footer(text=f"Page {page}/{len(pages)}")
                        await message.edit(embed=embed)
                        await message.remove_reaction("⬅", user)
                        await message.remove_reaction("➡", user)
                        await message.remove_reaction("❌", user)
                elif str(reaction.emoji) == "❌":
                    await message.delete()
                    return
            except asyncio.TimeoutError:
                await message.delete()
                return



