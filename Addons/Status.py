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
with open("Configs/status_config.yml", "r", encoding="utf-8") as file:
    status_config = yaml.load(file)

class Status(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        config_status = status_config['bot_activity']
        activity = discord.Game(name=status_config['bot_status_text'])
        await self.client.change_presence(status=config_status, activity=activity)
        print("[Status Addon] Addon Started - Bot Description Loaded!")


def setup(client):
    client.add_cog(Status(client))
