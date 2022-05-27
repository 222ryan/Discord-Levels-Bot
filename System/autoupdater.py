import asyncio
import os
import sys

import discord
from discord.ext import commands, tasks
from ruamel import yaml

import KumosLab.Database.get


with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)


bot_version = "2.0.4"

class autoupdater(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        if config['update_notify'] is True:
            update.start(self)

def setup(client):
    client.add_cog(autoupdater(client))

@tasks.loop(hours=24)
async def update(self = None):
    current_version = bot_version
    latest_version = await KumosLab.Database.get.latestVersion()
    if current_version != latest_version:
        bot_owner = self.client.get_user(int(config["Bot_Owner"]))
        embed = discord.Embed(title="📬 MODERN LEVELS - NEW UPDATE!", description="[A new update has been released for Modern Levels.](https://github.com/KumosLab/Discord-Levels-Bot)")
        embed.set_image(url="https://opengraph.githubassets.com/02c65877ccd391bd9b7f3b0e09154e1b9bdb321c2165d34026fc210fa1512f04/KumosLab/Discord-Levels-Bot")
        embed.add_field(name="Version", value=f"**~~{current_version}~~** `->` **{latest_version}**")
        embed.set_footer(text="React below to accept or decline the auto-update. Update will timeout after 1 hour.")
        await bot_owner.send(embed=embed)








