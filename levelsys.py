# Version 2.0 ALPHA // REQUIRES CONFIG VERSION 1.7 ALPHA

import discord
from discord.ext import commands
from pymongo import MongoClient
from ruamel.yaml import YAML

# MONGODB SETTINGS *YOU MUST FILL THESE OUT OTHERWISE YOU'LL RUN INTO ISSUES!*
cluster = MongoClient("mongodb link here - dont forget to insert password and database name!! and remove the <>")
levelling = cluster["databasename here"]["collectionsname here"]

yaml = YAML()
with open("./config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)

bot_channel = config['bot_channel']
talk_channels = config['talk_channels']
level_roles = config['level_roles']
level_roles_num = config['level_roles_num']


class levelsys(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id in config['talk_channels']:
            stats = levelling.find_one({"id": message.author.id})
            if not message.author.bot:
                if stats is None:
                    newuser = {"id": message.author.id, "tag": message.author.mention, "xp": 0, "rank": 1}
                    levelling.insert_one(newuser)
                else:
                    xp = stats["xp"] + config['xp_per_message']
                    levelling.update_one({"id": message.author.id}, {"$set": {"xp": xp}})
                    lvl = 0
                    while True:
                        if xp < ((config['xp_per_level'] / 2 * (lvl ** 2)) + (config['xp_per_level'] / 2 * lvl)):
                            break
                        lvl += 1
                    xp -= ((config['xp_per_level'] / 2 * ((lvl - 1) ** 2)) + (config['xp_per_level'] / 2 * (lvl - 1)))
                    if xp == 0:
                        levelling.update_one({"id": message.author.id}, {"$set": {"rank": lvl}})
                        embed2 = discord.Embed(title=f":tada: **LEVEL UP!**", description=f"{message.author.mention} just reached Level: **{lvl}**", colour=config['embed_colour'])
                        print(f"User: {message.author} | Leveled UP To: {lvl}")
                        embed2.add_field(name="XP:", value=f"``{xp}/{int(config['xp_per_level'] * 2 * ((1 / 2) * lvl))}``")
                        embed2.set_thumbnail(url=message.author.avatar_url)
                        await message.channel.send(embed=embed2)
                        for i in range(len(level_roles)):
                            if lvl == level_roles_num[i]:
                                await message.author.add_roles(
                                    discord.utils.get(message.author.guild.roles, name=level_roles[i]))
                                embed = discord.Embed(title=":tada: **ROLE UNLOCKED!**", description=f"{message.author.mention} has unlocked the **{level_roles[i]}** role!", colour=config['embed_colour'])
                                print(f"User: {message.author} | Unlocked Role: {level_roles[i]}")
                                embed.set_thumbnail(url=message.author.avatar_url)
                                await message.channel.send(embed=embed)

    # Rank Command
    @commands.command(aliases=config['rank_alias'])
    async def rank(self, ctx):
        if ctx.channel.id in config['bot_channel']:
            stats = levelling.find_one({"id": ctx.author.id})
            if stats is None:
                embed = discord.Embed(description=":x: You haven't sent any messages!", colour=config['error_embed_colour'])
                await ctx.channel.send(embed=embed)
            else:
                xp = stats["xp"]
                lvl = 0
                rank = 0
                while True:
                    if xp < ((config['xp_per_level'] / 2 * (lvl ** 2)) + (config['xp_per_level'] / 2 * lvl)):
                        break
                    lvl += 1
                xp -= ((config['xp_per_level'] / 2 * (lvl - 1)**2) + (config['xp_per_level'] / 2 * (lvl - 1)))
                boxes = int((xp / (config['xp_per_level'] * 2 * ((1 / 2) * lvl))) * 20)
                rankings = levelling.find().sort("xp", -1)
                for x in rankings:
                    rank += 1
                    if stats["id"] == x["id"]:
                        break
                embed = discord.Embed(title="{}'s Stats Menu | :bar_chart: ".format(ctx.author.name), colour=config['rank_embed_colour'])
                embed.add_field(name="Name", value=ctx.author.mention, inline=True)
                embed.add_field(name="XP", value=f"{xp + config['xp_per_message']}/{int(config['xp_per_level'] * 2 * ((1 / 2) * lvl))}",
                                inline=True)
                embed.add_field(name="Rank", value=f"{rank}/{ctx.guild.member_count}", inline=True)
                embed.add_field(name="Progress Bar",
                                value=boxes * config['completed_bar'] + (20 - boxes) * config['uncompleted_bar'],
                                inline=False)
                embed.add_field(name=f"Level", value=f"{lvl}", inline=False)
                embed.set_thumbnail(url=ctx.message.author.avatar_url)
                await ctx.channel.send(embed=embed)

    # Leaderboard Command
    @commands.command(aliases=config['leaderboard_alias'])
    async def leaderboard(self, ctx):
        if ctx.channel.id in bot_channel:
            rankings = levelling.find().sort("xp", -1)
            i = 1
            con = config['leaderboard_amount']
            embed = discord.Embed(title=f":trophy: Leaderboard | Top {con}", colour=config['leaderboard_embed_colour'])
            for x in rankings:
                try:
                    temp = ctx.guild.get_member(x["id"])
                    tempxp = x["xp"]
                    templvl = x["rank"]
                    embed.add_field(name=f"{i}: {temp.name}", value=f"Level: {templvl} | Total XP: {tempxp}", inline=False)
                    embed.set_thumbnail(url=config['leaderboard_image'])
                    i += 1
                except:
                    pass
                if i == config['leaderboard_amount']:
                    break
            await ctx.channel.send(embed=embed)

    # Reset Command
    @commands.command()
    @commands.has_role(config["admin_role"])
    async def reset(self, ctx, user):
        userget = user.replace('!', '')
        levelling.update_one({"tag": userget}, {"$set": {"rank": 1, "xp": 0}})
        embed = discord.Embed(title=f":white_check_mark: RESET USER", description=f"Reset User: {user}", colour=config['success_embed_colour'])
        await ctx.send(embed=embed)

    # Help Command
    @commands.command()
    async def help(self, ctx):
        if config['help_command'] == True:
            prefix = config['Prefix']
            top = config['leaderboard_amount']
            xp = config['xp_per_message']

            embed = discord.Embed(title="**Help Page | :book:**", description=f"Commands & Bot Settings. **Prefix**: {prefix}", colour=config["embed_colour"])
            embed.add_field(name="Leaderboard:", value=f"``{prefix}leaderboard`` *Shows the Top **{top}** users*")
            embed.add_field(name="Rank:", value=f"``{prefix}rank`` *Shows the Stats Menu for the user*")
            embed.add_field(name="Reset:", value=f"``{prefix}reset <user>`` *Sets a user back to XP: 0 and Level: 1*")
            embed.add_field(name="XP:", value=f"*You will earn ``{xp}xp`` per message*")
            embed.set_thumbnail(url=ctx.guild.icon_url)
            await ctx.channel.send(embed=embed)


def setup(client):
    client.add_cog(levelsys(client))
