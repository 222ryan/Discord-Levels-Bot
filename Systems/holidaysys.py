# Imports
from datetime import datetime
from random import random, randint

import discord
from discord.ext import commands
from ruamel.yaml import YAML
from Systems.levelsys import levelling

# Reads the config file, no need for changing.
yaml = YAML()
with open("Configs/holidayconfig.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)
with open("Configs/config.yml", "r", encoding="utf-8") as file2:
    config2 = yaml.load(file2)

current_month = datetime.now().month
current_day = datetime.now().day
current_year = datetime.now().year


# Spam system class
class seasonsys(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Started System: Holiday")
        print("------")
        print(f"Date: {current_day}/{current_month}/{current_year}")

    @commands.guild_only()
    @commands.command()
    async def event(self, ctx, holiday=None, state=None):
        if ctx.message.author.id != config2['bot_owner_id']:
            return
        else:
            if holiday == "Christmas":
                if state == "start":
                    for guild in self.client.guilds:
                        levelling.update_one({"server": guild.id}, {"$set": {"event": "Started"}})
                        embed = discord.Embed(title=":christmas_tree: **Christmas Holiday**",
                                              description=f"'Tis the season to be jolly! <@{self.client.user.id}> spreads Christmas cheer to all!", colour=0x0F7833)
                        embed.add_field(name=":gift: Present: ",
                                        value=f"`x{config['bonus_xp']}xp until {config['christmas_end_date']} {datetime.today().year + 1}`")
                        await guild.text_channels[0].send(embed=embed)
                elif state == "stop":
                    for guild in self.client.guilds:
                        levelling.update_one({"server": guild.id}, {"$set": {"event": "Ended"}})
                        embed = discord.Embed(title=":christmas_tree: **Christmas Holiday Over!**",
                                              description=f"The Christmas season is over.. We hope you had a great holiday full of joy!\n\n:gift: The **Present** `x{config['bonus_xp']}xp` has been reverted.", colour=0x0F7833)
                        await guild.text_channels[0].send(embed=embed)
                else:
                    embed = discord.Embed(title=":x: ***SOMETHING WENT WRONG!***", description="State must be either `start` or `stop`!")
                    await ctx.send(embed=embed)
            elif holiday == "Halloween":
                if state == "start":
                    for guild in self.client.guilds:
                        levelling.update_one({"server": guild.id}, {"$set": {"event": "Started"}})
                        house_number = randint(1, 99)
                        embed = discord.Embed(title=":jack_o_lantern: ***Spook Season***",
                                              description=f"Trick or Treat? Word has it, <@{self.client.user.id}> has the best treats at :house_abandoned: #{house_number}", colour=0xF75F1C)
                        embed.add_field(name=":candy: Treat: ",
                                        value=f"`x{config['bonus_xp']}xp until {config['halloween_end_date']} {datetime.today().year}`")
                        await guild.text_channels[0].send(embed=embed)
                elif state == "stop":
                    for guild in self.client.guilds:
                        levelling.update_one({"server": guild.id}, {"$set": {"event": "Ended"}})
                        embed = discord.Embed(title=":jack_o_lantern: **Halloween Scares are over!**",
                                              description=f"The Spooky season is over.. We hope you had a great Spooktober filled with scares!\n\n:candy: The **Treat** `x{config['bonus_xp']}xp` has been reverted.", colour=0xF75F1C)
                        await guild.text_channels[0].send(embed=embed)
                else:
                    embed = discord.Embed(title=":x: ***SOMETHING WENT WRONG!***", description="State must be either `start` or `stop`!")
                    await ctx.send(embed=embed)
            elif holiday == "Summer":
                if state == "start":
                    for guild in self.client.guilds:
                        levelling.update_one({"server": guild.id}, {"$set": {"event": "Started"}})
                        summer_embed = discord.Embed(title=":beach: **Summer Holiday**",
                                                     description=f"High tide or low tide, <@{self.client.user.id}> will stay by your side", colour=0xFFFE6F)
                        summer_embed.add_field(name=":icecream: Gift: ",
                                               value=f"`x{config['bonus_xp']}xp until {config['summer_end_date']} {datetime.today().year}`")
                        await guild.text_channels[0].send(embed=summer_embed)
                elif state == "stop":
                    for guild in self.client.guilds:
                        levelling.update_one({"server": guild.id}, {"$set": {"event": "Ended"}})
                        embed = discord.Embed(title=":beach: **Summer Holiday Over!**",
                                              description=f"The tides are down and the heat is going.. We hope you had a great summer!\n\n:icecream: The **Gift** `x{config['bonus_xp']}xp` has been reverted.", colour=0xFFFE6F)
                        await guild.text_channels[0].send(embed=embed)
                    return
                else:
                    embed = discord.Embed(title=":x: ***SOMETHING WENT WRONG!***", description="State must be either `start` or `stop`!")
                    await ctx.send(embed=embed)
            elif holiday == "Easter":
                if state == "start":
                    for guild in self.client.guilds:
                        levelling.update_one({"server": guild.id}, {"$set": {"event": "Started"}})
                        summer_embed = discord.Embed(title=":rabbit: **Easter Holiday**",
                                                     description=f"The Egg Hunt begins, <@{self.client.user.id}> has hidden Eggs all around your garden!", colour=0xee82ee)
                        summer_embed.add_field(name=":egg: Easter Egg Gift: ",
                                               value=f"`x{config['bonus_xp']}xp until {config['easter_end_date']} {datetime.today().year}`")
                        await guild.text_channels[0].send(embed=summer_embed)
                    return
                elif state == "stop":
                    for guild in self.client.guilds:
                        levelling.update_one({"server": guild.id}, {"$set": {"event": "Ended"}})
                        embed = discord.Embed(title=":rabbit: **Egg Hunt Over!**",
                                              description=f"Looks like all the eggs were found.. We hope you had a great Easter!\n\n:egg: The **Easter Egg Gift** `x{config['bonus_xp']}xp` has been reverted.", colour=0xee82ee)
                        await guild.text_channels[0].send(embed=embed)
                    return
                else:
                    embed = discord.Embed(title=":x: ***SOMETHING WENT WRONG!***", description="State must be either `start` or `stop`!")
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title=":x: ***SOMETHING WENT WRONG!***", description=f"`{holiday}` is not a valid holiday! Please chose from the list below:")
                embed.add_field(name="**Holidays**:", value=":beach: | `Summer`\n:egg: | `Easter`\n:jack_o_lantern: | `Halloween`\n:christmas_tree: | `Christmas`")
                await ctx.send(embed=embed)


# Sets-up the cog for antispam
def setup(client):
    client.add_cog(seasonsys(client))
