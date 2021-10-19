# Imports
import discord
from discord.ext import commands
from pymongo import MongoClient
from ruamel.yaml import YAML
import vacefron
import os
import re
from dotenv import load_dotenv

# Loads the .env file and gets the required information
load_dotenv()
MONGODB_URI = os.environ['MONGODB_URI']
COLLECTION = os.getenv("COLLECTION")
DB_NAME = os.getenv("DATABASE_NAME")

# Please enter your mongodb details in the .env file.
cluster = MongoClient(MONGODB_URI)
levelling = cluster[COLLECTION][DB_NAME]

# Reads the config file, no need for changing.
yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)
with open("Configs/spamconfig.yml", "r", encoding="utf-8") as file2:
    spamconfig = yaml.load(file2)
with open("Configs/holidayconfig.yml", "r", encoding="utf-8") as file2:
    holidayconfig = yaml.load(file2)


# Vac-API, no need for altering!
vac_api = vacefron.Client()


class levelsys(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, ctx):
        stats = levelling.find_one({"guildid": ctx.guild.id, "id": ctx.author.id})
        serverstats = levelling.find_one({"server": ctx.guild.id})
        bot_stats = levelling.find_one({"bot_name": self.client.user.name})
        if not ctx.author.bot:
            if stats is None:
                member = ctx.author
                user = f"<@{member.id}>"
                newuser = {"guildid": ctx.guild.id, "id": ctx.author.id, "tag": user, "xp": serverstats["xp_per_message"], "rank": 1, "background": " ", "circle": False, "xp_colour": "#ffffff", "name": f"{ctx.author}", "pfp": f"{ctx.author.avatar_url}", "warnings": 0}
                print(f"User: {ctx.author.id} has been added to the database! ")
                levelling.insert_one(newuser)
            else:
                talk_channels = serverstats['ignored_channels']
                if len(talk_channels) > 1 and ctx.channel.id not in talk_channels or config['Prefix'] in ctx.content:
                    stats = levelling.find_one({"guildid": ctx.guild.id, "id": ctx.author.id})
                    xp = stats["xp"]
                    levelling.update_one({"guildid": ctx.guild.id, "id": ctx.author.id}, {"$set": {"xp": xp}})
                elif len(talk_channels) < 1 or ctx.channel.id in talk_channels:
                    if bot_stats["event_state"] is True:
                        stats = levelling.find_one({"guildid": ctx.guild.id, "id": ctx.author.id})
                        xp = stats['xp'] + serverstats['xp_per_message'] * holidayconfig['bonus_xp']
                        levelling.update_one({"guildid": ctx.guild.id, "id": ctx.author.id}, {"$set": {"xp": xp}})
                    user = ctx.author
                    role = discord.utils.get(ctx.guild.roles, name=serverstats["double_xp_role"])
                    if role in user.roles:
                        stats = levelling.find_one({"guildid": ctx.guild.id, "id": ctx.author.id})
                        xp = stats["xp"] + serverstats['xp_per_message'] * 2
                        levelling.update_one({"guildid": ctx.guild.id, "id": ctx.author.id}, {"$set": {"xp": xp}})
                    else:
                        stats = levelling.find_one({"guildid": ctx.guild.id, "id": ctx.author.id})
                        xp = stats["xp"] + serverstats['xp_per_message']
                        levelling.update_one({"guildid": ctx.guild.id, "id": ctx.author.id}, {"$set": {"xp": xp}})

                xp = stats['xp']
                lvl = 0
                while True:
                    if xp < ((config['xp_per_level'] / 2 * (lvl ** 2)) + (config['xp_per_level'] / 2 * lvl)):
                        break
                    lvl += 1
                xp -= ((config['xp_per_level'] / 2 * ((lvl - 1) ** 2)) + (config['xp_per_level'] / 2 * (lvl - 1)))
                if stats["xp"] < 0:
                    levelling.update_one({"guildid": ctx.guild.id, "id": ctx.author.id}, {"$set": {"xp": 0}})
                if stats["rank"] != lvl:
                    levelling.update_one({"guildid": ctx.guild.id, "id": ctx.author.id}, {"$set": {"rank": lvl + 1}})
                    embed2 = discord.Embed(title=f":tada: **LEVEL UP!**",
                                           description=f"{ctx.author.mention} just reached Level: **{lvl}**",
                                           colour=config['embed_colour'])
                    xp = stats["xp"]
                    levelling.update_one({"guildid": ctx.guild.id, "id": ctx.author.id},
                                         {"$set": {"rank": lvl, "xp": xp + serverstats['xp_per_message'] * 2}})
                    print(f"User: {ctx.author} | Leveled UP To: {lvl}")
                    embed2.add_field(name="Next Level:",
                                     value=f"`{int(config['xp_per_level'] * 2 * ((1 / 2) * lvl))}xp`")
                    embed2.set_thumbnail(url=ctx.author.avatar_url)
                    member = ctx.author
                    channel = discord.utils.get(member.guild.channels, name=serverstats["level_channel"])
                    if config['level_up_ping'] is True:
                        await channel.send(f"{ctx.author.mention}")
                    msg = await channel.send(embed=embed2)
                    level_roles = serverstats["role"]
                    level_roles_num = serverstats["level"]
                    for i in range(len(level_roles)):
                        if lvl == int(level_roles_num[i]):
                            await ctx.author.add_roles(
                                discord.utils.get(ctx.author.guild.roles, name=level_roles[i]))
                            await ctx.author.remove_roles(discord.utils.get(ctx.author.guild.roles, name=level_roles[i-1]))
                            embed = discord.Embed(title=":tada: **LEVEL UP**",
                                                  description=f"{ctx.author.mention} just reached Level: **{lvl}**",
                                                  colour=config['embed_colour'])
                            embed.add_field(name="Next Level:",
                                            value=f"`{int(config['xp_per_level'] * 2 * ((1 / 2) * lvl))}xp`")
                            embed.add_field(name="Role Unlocked", value=f"`{level_roles[i]}`")
                            print(f"User: {ctx.author} | Unlocked Role: {level_roles[i]}")
                            embed.set_thumbnail(url=ctx.author.avatar_url)
                            await msg.edit(embed=embed)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        serverstats = levelling.find_one({"server": guild.id})
        if serverstats is None:
            newserver = {"server": guild.id, "xp_per_message": 10, "double_xp_role": "None",
                         "level_channel": "private",
                         "Antispam": False, "mutedRole": "None", "mutedTime": 300, "warningMessages": 5,
                         "muteMessages": 6,
                         "ignoredRole": "None", "event": "Ended", "ignored_channels": []}
            if config['private_message'] is True:
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    guild.me: discord.PermissionOverwrite(read_messages=True)
                }
                levelling.insert_one(newserver)
                prefix = config['Prefix']
                embed = discord.Embed(title=f"👋 // Greetings, {guild.name}", description=f"Thanks for inviting me, my prefix here is: `{prefix}`")
                if os.path.exists("Addons/Extras+.py") is True:
                    embed.add_field(name="🚀 | What's Next?", value=f"`{prefix}help` displays every command you need to know for {self.client.user.mention}", inline=False)
                embed.add_field(name="🧭 | Important Links:", value=f"[Support Server](https://www.discord.gg/E56eZdNjK4) - Get support for {self.client.user.mention}")
                if guild.system_channel is None:
                    await guild.create_text_channel('private', overwrites=overwrites)
                    channel = discord.utils.get(guild.channels, name="private")
                    await channel.send(embed=embed)
                else:
                    await guild.system_channel.send(embed=embed)
        for member in guild.members:
            if not member.bot:
                newuser = {"guildid": member.guild.id, "id": member.id, "tag": f"<@{member.id}>",
                           "xp": 10,
                           "rank": 1, "background": " ", "circle": False, "xp_colour": "#ffffff", "warnings": 0}
                levelling.insert_one(newuser)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        # Removes the server from the database
        levelling.delete_one({"server": guild.id})

        # Deletes all users when they bot is removed from the server
        for member in guild.members:
            if not member.bot:
                levelling.delete_one({"guildid": guild.id, "id": member.id})


    @commands.Cog.listener()
    async def on_member_join(self, member):
        if not member.bot:
            getGuild = levelling.find_one({"server": member.guild.id})
            newuser = {"guildid": member.guild.id, "id": member.id, "tag": f"<@{member.id}>", "xp": getGuild["xp_per_message"],
                       "rank": 1, "background": " ", "circle": False, "xp_colour": "#ffffff", "warnings": 0}
            levelling.insert_one(newuser)
            print(f"User: {member.id} has been added to the database!")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if not member.bot:
            levelling.delete_one({"server": member.guild.id, "id": member.id})
            print(f"User: {member.id} has been removed from the database!")


def setup(client):
    client.add_cog(levelsys(client))

# End Of Level System
