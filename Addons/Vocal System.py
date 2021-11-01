import asyncio
import os

import discord
from discord.ext import commands
from ruamel.yaml import YAML
from Systems.levelsys import levelling

yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)


# Spam system class
class Vocal(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_voice_state_update(self, member : discord.Member, before, after):
        if before.channel is None and after.channel is not None:
            try:
                while True:
                    if after.afk:
                        return
                    await asyncio.sleep(config['time_for_xp'])
                    if after.channel is None:
                        return
                    guild = member.guild
                    stats = levelling.find_one({"guildid": guild.id, "id": member.id})
                    xp = stats['xp']
                    levelling.update_one({"guildid": guild.id, "id": member.id}, {"$set": {"xp": xp + config['xp_per_time']}})
                    if os.path.exists("Addons/Clan System.py") is True:
                        clan_search = levelling.find_one({"guildid": member.guild.id, "users": f"{member}"})
                        if clan_search:
                            levelling.update_one({"guildid": member.guild.id, "clan_name": clan_search['clan_name']}, {"$set": {"total_xp": clan_search['total_xp'] + config['xp_per_time']}})
                            for x in clan_search['users']:
                                if x == str(member):
                                    continue
                                elif x != str(member):
                                    stats = levelling.find_one({"guildid": member.guild.id, "name": x})
                                    levelling.update_one({"guildid": member.guild.id, "name": x}, {"$set": {
                                        "xp": stats['xp'] + config['xp_per_time'] / 2}})

            except Exception as e:
                print(e)


# Sets-up the cog for Profile+
def setup(client):
    client.add_cog(Vocal(client))
