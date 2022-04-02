import asyncio
import os
import sys

import discord
from discord.ext import commands, tasks
from ruamel import yaml

import KumosLab.Database.get


with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)


bot_version = "2.0.0"

class autoupdater(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        update.start(self)

    async def do_update(self):
        latest_version = await KumosLab.Database.get.latestVersion()
        link = "https://github.com/KumosLab/Discord-Levels-Bot.git"
        print("Updating...")
        os.system("git init")
        os.system("git remote add origin " + link)
        os.system(f"git pull origin {latest_version}")
        os.system(f"git reset --mixed {latest_version}")


        bot_owner = self.client.get_user(int(config["Bot_Owner"]))
        await bot_owner.send("`🟢` | Update installed, the bot will now shutdown..")

        exit("Update Installed - Please restart me!")

def setup(client):
    client.add_cog(autoupdater(client))

@tasks.loop(minutes=30)
async def update(self = None):
    current_version = bot_version
    latest_version = await KumosLab.Database.get.latestVersion()
    if current_version != latest_version:
        bot_owner = self.client.get_user(int(config["Bot_Owner"]))
        embed = discord.Embed(title="📬 MODERN LEVELS - NEW UPDATE!", description="[A new update has been released for Modern Levels.](https://github.com/KumosLab/Discord-Levels-Bot)")
        embed.set_image(url="https://opengraph.githubassets.com/02c65877ccd391bd9b7f3b0e09154e1b9bdb321c2165d34026fc210fa1512f04/KumosLab/Discord-Levels-Bot")
        embed.add_field(name="Version", value=f"**~~{current_version}~~** `->` **{latest_version}**")
        embed.set_footer(text="React below to accept or decline the auto-update. Update will timeout after 1 hour.")
        message = await bot_owner.send(embed=embed)

        await message.add_reaction("✅")
        await message.add_reaction("❌")

        def check(reaction, user):
            return user == bot_owner and reaction.message.id == message.id

        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=3600.0, check=check)

            if reaction.emoji == "✅":
                # remove all reactions
                await bot_owner.send("`🟢` | Update confirmed, starting installation..")
                await autoupdater.do_update(self=self)


            elif reaction.emoji == "❌":
                # remove all reactions
                await bot_owner.send('`🔴` | Update cancelled by user, please download manually.')
                update.stop()



        except asyncio.TimeoutError:
            await bot_owner.send('`🔴` | Update timed out, please download manually.')
            update.stop()








