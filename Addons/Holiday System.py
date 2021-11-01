# Imports
import math
from datetime import datetime
from random import randint

import discord
from dateutil.easter import *
from discord.ext import commands, tasks
from ruamel.yaml import YAML

# Reads the config file, no need for changing.
from Systems.levelsys import levelling

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

        @tasks.loop(minutes=1)
        async def e():
            bot_stats = levelling.find_one({"bot_name": self.client.user.name})
            active_servers = self.client.guilds

            # Halloween Check
            if datetime.now().month == 10:
                if datetime.now().day == config['halloween_start_date']:
                    if bot_stats['event_state'] is True:
                        return
                    else:
                        for guild in active_servers:
                            serverstats = levelling.find_one({"server": guild.id})
                            house_number = randint(1, 99)
                            embed = discord.Embed(title=":jack_o_lantern: // **Spook Season**",
                                                  description=f"Trick or Treat? Word has it, <@{self.client.user.id}> has the best treats at `🏚️ House #{house_number}`",
                                                  colour=0xF75F1C)
                            embed.add_field(name=":candy: Treat: ",
                                            value=f"`x{config['bonus_xp']}xp until 1st of November, {datetime.today().year}`")
                            channel = discord.utils.get(guild.channels, name=serverstats["level_channel"])
                            if channel is None:
                                continue
                            await channel.send(embed=embed)
                        levelling.update_one({"bot_name": self.client.user.name}, {"$set": {"event_state": True}})
                        print("Halloween Event has started! Servers will receive a message shortly!")
            elif datetime.now().month == 11:
                if bot_stats['event_state'] is False:
                    return
                else:
                    embed = discord.Embed(title=":jack_o_lantern: **Halloween Scares are over!**",
                                          description=f"The Spooky season is over.. We hope you had a great Spooktober filled with scares!\n\n:candy: The **Treat** `x{config['bonus_xp']}xp` has been reverted.",
                                          colour=0xF75F1C)
                    levelling.update_one({"bot_name": self.client.user.name}, {"$set": {"event_state": False}})
                    for guild in active_servers:
                        serverstats = levelling.find_one({"server": guild.id})
                        channel = discord.utils.get(guild.channels, name=serverstats["level_channel"])
                        if channel is None:
                            continue
                        await channel.send(embed=embed)

            # Christmas Check
            if datetime.now().month == 12:
                if datetime.now().day == config['christmas_start_date']:
                    if bot_stats['event_state'] is True:
                        return
                    else:
                        for guild in active_servers:
                            serverstats = levelling.find_one({"server": guild.id})
                            embed = discord.Embed(title=":christmas_tree: // **Christmas Holiday**",
                                                  description=f"Tis the season to be jolly! <@{self.client.user.id}> spreads Christmas cheer to all!",
                                                  colour=0x0F7833)
                            embed.add_field(name=":gift: Present: ",
                                            value=f"`x{config['bonus_xp']}xp until 1st of January, {datetime.today().year + 1}`")
                            channel = discord.utils.get(guild.channels, name=serverstats["level_channel"])
                            if channel is None:
                                continue
                            await channel.send(embed=embed)
                        levelling.update_one({"bot_name": self.client.user.name}, {"$set": {"event_state": True}})
                        print("Christmas Event has started! Servers will receive a message shortly!")
            elif datetime.now().month == 1:
                if bot_stats['event_state'] is False:
                    return
                else:
                    levelling.update_one({"bot_name": self.client.user.name}, {"$set": {"event_state": False}})
                    embed = discord.Embed(title=":christmas_tree: **Christmas Holiday Over!**",
                                          description=f"The Christmas season is over.. We hope you had a great holiday full of joy!\n\n:gift: The **Present** `x{config['bonus_xp']}xp` has been reverted.",
                                          colour=0x0F7833)
                    for guild in active_servers:
                        serverstats = levelling.find_one({"server": guild.id})
                        channel = discord.utils.get(guild.channels, name=serverstats["level_channel"])
                        if channel is None:
                            continue
                        await channel.send(embed=embed)

            # Easter Check
            if datetime.now().month == 4:
                if datetime.now().day == config['easter_start_date']:
                    if bot_stats['event_state'] is True:
                        return
                    else:
                        for guild in active_servers:
                            serverstats = levelling.find_one({"server": guild.id})
                            embed = discord.Embed(title=":rabbit: // **Easter Holiday**",
                                                  description=f"The Egg Hunt begins, <@{self.client.user.id}> has hidden Eggs all around your garden!",
                                                  colour=0xee82ee)
                            embed.add_field(name=":egg: Easter Egg Gift: ",
                                            value=f"`x{config['bonus_xp']}xp until 1st of March, {datetime.today().year}`")
                            channel = discord.utils.get(guild.channels, name=serverstats["level_channel"])
                            if channel is None:
                                continue
                            await channel.send(embed=embed)
                        levelling.update_one({"bot_name": self.client.user.name}, {"$set": {"event_state": True}})
                        print("Easter Event has started! Servers will receive a message shortly!")
            elif datetime.now().month == 5:
                if bot_stats['event_state'] is False:
                    return
                else:
                    levelling.update_one({"bot_name": self.client.user.name}, {"$set": {"event_state": False}})
                    embed = discord.Embed(title=":rabbit: **Egg Hunt Over!**",
                                          description=f"Looks like all the eggs were found.. We hope you had a great Easter!\n\n:egg: The **Easter Egg Gift** `x{config['bonus_xp']}xp` has been reverted.",
                                          colour=0xee82ee)

                    for guild in active_servers:
                        serverstats = levelling.find_one({"server": guild.id})
                        channel = discord.utils.get(guild.channels, name=serverstats["level_channel"])
                        if channel is None:
                            continue
                        await channel.send(embed=embed)

            # Summer Check
            if datetime.now().month == 7:
                if datetime.now().day == config['summer_start_date']:
                    if bot_stats['event_state'] is True:
                        return
                    else:
                        for guild in active_servers:
                            serverstats = levelling.find_one({"server": guild.id})
                            embed = discord.Embed(title=":beach: // **Summer Holiday**",
                                                  description=f"High tide or low tide, <@{self.client.user.id}> will stay by your side",
                                                  colour=0xFFFE6F)
                            embed.add_field(name=":icecream: Gift: ",
                                            value=f"`x{config['bonus_xp']}xp until 1st of September, {datetime.today().year}`")
                            channel = discord.utils.get(guild.channels, name=serverstats["level_channel"])
                            if channel is None:
                                continue
                            await channel.send(embed=embed)
                        levelling.update_one({"bot_name": self.client.user.name}, {"$set": {"event_state": True}})
                        print("Summer Event has started! Servers will receive a message shortly!")
            elif datetime.now().month == 9:
                if bot_stats['event_state'] is False:
                    return
                else:
                    levelling.update_one({"bot_name": self.client.user.name}, {"$set": {"event_state": False}})
                    embed = discord.Embed(title=":rabbit: **Egg Hunt Over!**",
                                          description=f"Looks like all the eggs were found.. We hope you had a great Easter!\n\n:egg: The **Easter Egg Gift** `x{config['bonus_xp']}xp` has been reverted.",
                                          colour=0xee82ee)
                    for guild in active_servers:
                        serverstats = levelling.find_one({"server": guild.id})
                        channel = discord.utils.get(guild.channels, name=serverstats["level_channel"])
                        if channel is None:
                            continue
                        await channel.send(embed=embed)

            # Check if date is holiday date (e.g december 25th)
            if datetime.now().month == 12:
                if datetime.now().day == 25:
                    for guild in active_servers:
                        stats = levelling.find_one({"bot_name": self.client.user.name, "day": False})
                        if stats:
                            levelling.update_one({"server": guild.id}, {"$set": {"day": True}})
                            serverstats = levelling.find_one({"server": guild.id})
                            channel = discord.utils.get(guild.channels, name=serverstats["level_channel"])
                            if channel is None:
                                continue
                            else:
                                embed = discord.Embed(title="☃️ MERRY CHRISTMAS!",
                                                      description=f"{self.client.user.mention} wishes you all a Merry Christmas!",
                                                      colour=0x0F7833)
                                await channel.send(embed=embed)
                        elif not stats:
                            return
            elif datetime.now().month == 9:
                if datetime.now().day == easter(current_year).day:
                    for guild in active_servers:
                        stats = levelling.find_one({"bot_name": self.client.user.name, "day": False})
                        if stats:
                            levelling.update_one({"server": guild.id}, {"$set": {"day": True}})
                            serverstats = levelling.find_one({"server": guild.id})
                            channel = discord.utils.get(guild.channels, name=serverstats["level_channel"])
                            if channel is None:
                                continue
                            else:
                                embed = discord.Embed(title="🐰 HAPPY EASTER!",
                                                      description=f"{self.client.user.mention} wishes you all a Happy Easter!",
                                                      colour=0xee82ee)
                                await channel.send(embed=embed)
                        elif not stats:
                            return
            elif datetime.now().month == 10:
                if datetime.now().day == 31:
                    for guild in active_servers:
                        stats = levelling.find_one({"bot_name": self.client.user.name, "day": False})
                        if stats:
                            levelling.update_one({"bot_name": self.client.user.name}, {"$set": {"day": True}})
                            serverstats = levelling.find_one({"server": guild.id})
                            channel = discord.utils.get(guild.channels, name=serverstats["level_channel"])
                            if channel is None:
                                continue
                            else:
                                embed = discord.Embed(title="🎃 HAPPY HALLOWEEN!",
                                                      description=f"{self.client.user.mention} wishes you all a Scary Halloween full of goods!",
                                                      colour=0xF75F1C)
                                await channel.send(embed=embed)
                        elif not stats:
                            return
            elif datetime.now().month == 7:
                if datetime.now().day == 12:
                    for guild in active_servers:
                        stats = levelling.find_one({"bot_name": self.client.user.name, "day": False})
                        if stats:
                            levelling.update_one({"bot_name": self.client.user.name}, {"$set": {"day": True}})
                            serverstats = levelling.find_one({"server": guild.id})
                            channel = discord.utils.get(guild.channels, name=serverstats["level_channel"])
                            if channel is None:
                                continue
                            else:
                                embed = discord.Embed(title="🏖️ SUMMER TIME!",
                                                      description=f"{self.client.user.mention} wishes you all a Warm Summer!",
                                                      colour=0xFFFE6F)
                                await channel.send(embed=embed)
                        elif not stats:
                            return
            else:
                stats = levelling.find_one({"bot_name": self.client.user.name, "day": False})
                if stats is None:
                    levelling.update_one({"bot_name": self.client.user.name}, {"$set": {"day": False}})
                    return

        e.start()

    @commands.command()
    async def countdown(self, ctx):
        month = datetime.now()
        month = month.strftime("%B")
        if month == "November" or month == "December":
            christmas = datetime.strptime(f"12/25/{current_year}", "%m/%d/%Y")
            now = datetime.now()
            diff = christmas - now
            days = diff.days
            seconds = int(diff.seconds)
            hours = int(math.floor(seconds / 3600))
            minutes = int(math.floor((seconds - (hours * 3600)) / 60))
            secs = seconds - (hours * 3600) - (minutes * 60)
            strHours = str(hours)
            strMinutes = str(minutes)
            strSeconds = str(secs)
            christmas_embed = discord.Embed(title="🎅 CHRISTMAS COUNTDOWN!",
                                            description=f"The Christmas season is coming, so to get into the spirit, here's a Christmas Countdown.",
                                            colour=0xc54245)
            christmas_embed.add_field(name="Days:", value=f"`{days}`", inline=True)
            christmas_embed.add_field(name="Hours:", value=f"`{strHours}`", inline=True)
            christmas_embed.add_field(name="Minutes:", value=f"`{strMinutes}`", inline=True)
            christmas_embed.add_field(name="Seconds:", value=f"`{strSeconds}`", inline=True)
            christmas_embed.set_image(
                url="https://www.rd.com/wp-content/uploads/2018/10/this-is-why-christmas-is-on-deember-25.jpg?resize=768,512")
            christmas_embed.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/831180817064656907/890737461033054268/Santa_PNG_Clipart-54.png")
            await ctx.send(embed=christmas_embed)
        elif month == "October":
            halloween = datetime.strptime(f"10/31/{current_year}", "%m/%d/%Y")
            now = datetime.now()
            diff = halloween - now
            days = diff.days
            seconds = int(diff.seconds)
            hours = int(math.floor(seconds / 3600))
            minutes = int(math.floor((seconds - (hours * 3600)) / 60))
            secs = seconds - (hours * 3600) - (minutes * 60)
            strHours = str(hours)
            strMinutes = str(minutes)
            strSeconds = str(secs)
            halloween_embed = discord.Embed(title="🎃 HALLOWEEN COUNTDOWN!",
                                            description=f"The Spooky season season is coming, so to begin the scares, here's a Halloween Countdown.",
                                            colour=0xeb6123)
            halloween_embed.add_field(name="Days:", value=f"`{days}`", inline=True)
            halloween_embed.add_field(name="Hours:", value=f"`{strHours}`", inline=True)
            halloween_embed.add_field(name="Minutes:", value=f"`{strMinutes}`", inline=True)
            halloween_embed.add_field(name="Seconds:", value=f"`{strSeconds}`", inline=True)
            halloween_embed.set_image(
                url="https://cdn.pixabay.com/photo/2017/10/10/16/55/halloween-2837936_960_720.png")
            halloween_embed.set_thumbnail(url="http://pngimg.com/uploads/halloween/halloween_PNG189.png")
            await ctx.send(embed=halloween_embed)
        elif month == "January" or "February" or "March" or "April":
            easter_day = easter(current_year).day
            easter_date = datetime.strptime(f"04/{easter_day}/{current_year}", "%m/%d/%Y")
            now = datetime.now()
            diff = easter_date - now
            days = diff.days
            seconds = int(diff.seconds)
            hours = int(math.floor(seconds / 3600))
            minutes = int(math.floor((seconds - (hours * 3600)) / 60))
            secs = seconds - (hours * 3600) - (minutes * 60)
            strHours = str(hours)
            strMinutes = str(minutes)
            strSeconds = str(secs)
            easter_embed = discord.Embed(title="🐰 EASTER COUNTDOWN!",
                                         description=f"The Egg Hunts begin soon! For the mean time, here's an Easter Countdown.",
                                         colour=0xe9aad1)
            easter_embed.add_field(name="Days:", value=f"`{days}`", inline=True)
            easter_embed.add_field(name="Hours:", value=f"`{strHours}`", inline=True)
            easter_embed.add_field(name="Minutes:", value=f"`{strMinutes}`", inline=True)
            easter_embed.add_field(name="Seconds:", value=f"`{strSeconds}`", inline=True)
            easter_embed.set_image(url="https://i.pinimg.com/originals/8f/a7/fd/8fa7fd6e48518d1dbaa9c55eeecf7400.png")
            easter_embed.set_thumbnail(url="http://pngimg.com/uploads/halloween/halloween_PNG189.png")
            await ctx.send(embed=easter_embed)


# Sets-up the cog for antispam
def setup(client):
    client.add_cog(seasonsys(client))
