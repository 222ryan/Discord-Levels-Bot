# Imports
import asyncio
import discord
from discord.ext import commands
from pymongo import MongoClient
from ruamel.yaml import YAML
import vacefron
import os
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


# Some config options which need to be stored here, again, no need for altering.


# Vac-API, no need for altering!
vac_api = vacefron.Client()


class levelsys(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, ctx):
        stats = levelling.find_one({"guildid": ctx.guild.id, "id": ctx.author.id})
        serverstats = levelling.find_one({"server": ctx.guild.id})
        if not ctx.author.bot:
            if serverstats is None:
                newserver = {"server": ctx.guild.id, "xp_per_message": 10, "double_xp_role": "NA", "level_channel": "private"}
                overwrites = {
                    ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    ctx.guild.me: discord.PermissionOverwrite(read_messages=True)
                }
                await ctx.guild.create_text_channel('private', overwrites=overwrites)
                levelling.insert_one(newserver)
                member = ctx.author
                serverstat = levelling.find_one({"server": ctx.guild.id})
                channel = discord.utils.get(member.guild.channels, name=serverstat["level_channel"])
                prefix = config['Prefix']
                await channel.send(f"> Hey!\n\n You will only see this message **once**. To change the channel where levelup messages get sent to:\n\n`{prefix}levelchannel <channelname>` -- Please do NOT use the hashtag and enter any -'s!\n\nYou can also set a role which earns 2x XP by doing the following:\n\n`{prefix}doublexp <rolename>`\n\nYou can also add or remove roles after levelling up by doing the following\n\n`{prefix}role <add|remove> <level> <rolename>`\n\nYou can also change how much xp you earn per message by doing:\n\n`{prefix}xppermessage <amount>`\n\nFor help with commands:\n\n`{prefix}help` ")
            if stats is None:
                newuser = {"guildid": ctx.guild.id, "id": ctx.author.id, "tag": ctx.author.mention, "xp": serverstats["xp_per_message"], "rank": 1, "background": " ", "circle": False, "xp_colour": "#ffffff", "name": f"{ctx.author}", "pfp": f"{ctx.author.avatar_url}"}
                print(f"User: {ctx.author.id} has been added to the database! ")
                levelling.insert_one(newuser)
            else:
                if config['Prefix'] in ctx.content:
                    stats = levelling.find_one({"guildid": ctx.guild.id, "id": ctx.author.id})
                    xp = stats["xp"]
                    levelling.update_one({"guildid": ctx.guild.id, "id": ctx.author.id}, {"$set": {"xp": xp}})
                else:
                    stats = levelling.find_one({"server": ctx.guild.id})
                    if stats is None:
                        return
                    else:
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
                levelling.update_one({"guildid": ctx.guild.id, "id": ctx.author.id}, {'$set': {"pfp": f"{ctx.author.avatar_url}", "name": f"{ctx.author}"}})
                lvl = 0
                while True:
                    if xp < ((config['xp_per_level'] / 2 * (lvl ** 2)) + (config['xp_per_level'] / 2 * lvl)):
                        break
                    lvl += 1
                xp -= ((config['xp_per_level'] / 2 * ((lvl - 1) ** 2)) + (config['xp_per_level'] / 2 * (lvl - 1)))
                if xp == 0:
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
                    msg = await channel.send(embed=embed2)
                    level_roles = serverstats["role"]
                    level_roles_num = serverstats["level"]
                    channel = discord.utils.get(member.guild.channels, name=serverstats['level_channel'])
                    for i in range(len(level_roles)):
                        if lvl == level_roles_num[i]:
                            await ctx.author.add_roles(
                                discord.utils.get(ctx.author.guild.roles, name=level_roles[i]))
                            embed = discord.Embed(title=":tada: **LEVEL UP**",
                                                  description=f"{ctx.author.mention} just reached Level: **{lvl}**",
                                                  colour=config['embed_colour'])
                            embed.add_field(name="Next Level:",
                                            value=f"`{int(config['xp_per_level'] * 2 * ((1 / 2) * lvl))}xp`")
                            embed.add_field(name="Role Unlocked", value=f"`{level_roles[i]}`")
                            print(f"User: {ctx.author} | Unlocked Role: {level_roles[i]}")
                            embed.set_thumbnail(url=ctx.author.avatar_url)
                            await msg.edit(embed=embed)
                        for i in range(len(level_roles)):
                            if lvl == level_roles_num[i]:
                                await ctx.author.add_roles(
                                    discord.utils.get(ctx.author.guild.roles, name=level_roles[i]))
                                embed = discord.Embed(title=":tada: **LEVEL UP**",
                                                      description=f"{ctx.author.mention} just reached Level: **{lvl}**",
                                                      colour=config['embed_colour'])
                                embed.add_field(name="Next Level:",
                                                 value=f"`{int(config['xp_per_level'] * 2 * ((1 / 2) * lvl))}xp`")
                                embed.add_field(name="Role Unlocked", value=f"`{level_roles[i]}`")
                                print(f"User: {ctx.author} | Unlocked Role: {level_roles[i]}")
                                embed.set_thumbnail(url=ctx.author.avatar_url)
                                await msg.edit(embed=embed)


def setup(client):
    client.add_cog(levelsys(client))

# End Of Level System
