import asyncio
import os

import discord
from discord.ext import commands
from ruamel.yaml import YAML

import KumosLab.Database.get
import KumosLab.Database.add
import KumosLab.Database.check

yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)
with open("Configs/vocal_config.yml", "r", encoding="utf-8") as file:
    vocal_config = yaml.load(file)

class Vocal(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("[Vocal Addon] Addon Started - Join a VC to earn XP!")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before, after):
        if before.channel is None and after.channel is not None:
            try:
                while True:
                    if after.afk:
                        return
                    await asyncio.sleep(vocal_config["waiting_time"])
                    if after.channel is None:
                        return
                    guild = member.guild
                    await KumosLab.Database.add.xp(user=member, guild=guild, amount=vocal_config["xp_per_time"])
                    await KumosLab.Database.check.levelUp(user=member, guild=guild)

            except Exception as e:
                print("[Vocal Addon] " + str(e))
                return

def setup(client):
    client.add_cog(Vocal(client))
