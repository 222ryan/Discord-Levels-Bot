import asyncio
import os
from os import listdir
import sys

import discord
from discord.ext import commands, tasks
from ruamel import yaml

import KumosLab.Database.get


with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)


class addonmanager(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def addons(self, ctx):
        addons = []
        for file in listdir("Addons"):
            if file.endswith(".py"):
                addons.append(file.replace(".py", ""))

        if len(addons) == 0:
            embed = discord.Embed(title="Installed Addons", description="```No addons installed!```")
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(title="Installed Addons", description=f"```{addons}```".replace("[", "").replace("]", "").replace("'", ""))
            await ctx.reply(embed=embed)


    @commands.command()
    async def addon(self, ctx, addon: str = None):
        if ctx.author.id == int(config['Bot_Owner']):
            if addon is None:
                embed = discord.Embed(title="📬 ADDON MANAGER")
                embed.add_field(name="📢 Vocal", value=f"`{config['Prefix']}addon vocal`", inline=False)
                embed.add_field(name="➕ Extras", value=f"`{config['Prefix']}addon extras`", inline=False)
                embed.add_field(name="👤 Status", value=f"`{config['Prefix']}addon status`", inline=False)
                await ctx.reply(embed=embed)
            else:
                if addon.title() not in ["Vocal", "Clan", "Extras", "Status", "Prestige"]:
                    await ctx.reply("❌ **Addon not found**")
                else:
                    link = "https://github.com/KumosLab/Discord-Levels-Bot.git"
                    branch = addon.title()

                    # git init into Downloads
                    os.system(f"git init Downloads")
                    os.system(f"cd Downloads && git remote add origin {link}")
                    os.system(f"cd Downloads && git pull origin {branch}")
                    os.system(f"cd Downloads && git checkout {branch}")
                    os.system(f"cd Downloads && git pull")




                    # get absolute path of Downloads
                    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Downloads/Addons"))
                    path2 = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Downloads/Configs"))
                    # get absolute path of addon folder
                    addon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Addons"))
                    # get absolute path of configs folder
                    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Configs"))

                    # for files in path 1 move to addon_path
                    for file in listdir(path):
                        os.replace(os.path.join(path, file), os.path.join(addon_path, file))

                    # for files in path 2 move to config_path
                    for file in listdir(path2):
                        os.replace(os.path.join(path2, file), os.path.join(config_path, file))

                    await ctx.reply("`🟢` | Addon installed, starting addon...")
                    for fn in listdir("Addons"):
                        if fn.endswith(".py"):
                            try:
                                self.client.load_extension(f"Addons.{addon.title()}")
                                await ctx.reply("`🟢` | Addon started")
                                break
                            except Exception as e:
                                self.client.reload_extension(f"Addons.{addon.title()}")
                                await ctx.reply("`🟢` | Addon started")
                                break


        else:
            return





def setup(client):
    client.add_cog(addonmanager(client))







