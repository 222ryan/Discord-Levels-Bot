import discord
from discord.ext import commands
from pymongo import MongoClient
from ruamel.yaml import YAML

cluster = MongoClient("mongodb link here - dont forget to insert password and database name!! and remove the <>")
levelling = cluster["database"]["collection"]  # Example: discord.levelling would be ["discord"]["levelling"]

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
    async def on_ready(self):
        print("Online!")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id in config['talk_channels']:
            stats = levelling.find_one({"id": message.author.id})
            if not message.author.bot:
                if stats is None:
                    newuser = {"id": message.author.id, "xp": 0, "rank": 1}
                    levelling.insert_one(newuser)
                else:
                    xp = stats["xp"] + config['xp_per_message']
                    levelling.update_one({"id": message.author.id}, {"$set": {"xp": xp}})
                    lvl = 0
                    while True:
                        if xp < ((50 *(lvl**2))+(50*lvl)):
                            break
                        lvl += 1
                    xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
                    if xp == 0:
                        levelling.update_one({"id": message.author.id}, {"$set": {"rank": lvl}})
                        embed2 = discord.Embed(description=f"{message.author.mention} just reached Level: **{lvl}**")
                        embed2.set_thumbnail(url=message.author.avatar_url)
                        await message.channel.send(embed=embed2)
                        for i in range(len(level_roles)):
                            if lvl == level_roles_num[i]:
                                await message.author.add_roles(
                                    discord.utils.get(message.author.guild.roles, name=level_roles[i]))
                                embed = discord.Embed(
                                    description=f"{message.author.mention} you have unlocked the **{level_roles[i]}** role!")
                                embed.set_thumbnail(url=message.author.avatar_url)
                                await message.channel.send(embed=embed)

    @commands.command()
    async def rank(self, ctx):
        if ctx.channel.id == config['bot_channel']:
            stats = levelling.find_one({"id": ctx.author.id})
            if stats is None:
                embed = discord.Embed(description=":x: You haven't sent any messages!")
                await ctx.channel.send(embed=embed)
            else:
                xp = stats["xp"]
                lvl = 0
                rank = 0
                while True:
                    if xp < ((50 * (lvl ** 2)) + (50 * lvl)):
                        break
                    lvl += 1
                xp -= ((50 * (lvl - 1)**2) + (50 * (lvl - 1)))
                boxes = int((xp / (200 * ((1 / 2) * lvl))) * 20)
                rankings = levelling.find().sort("xp", -1)
                for x in rankings:
                    rank += 1
                    if stats["id"] == x["id"]:
                        break
                embed = discord.Embed(title="{}'s Stats Menu | :bar_chart: ".format(ctx.author.name))
                embed.add_field(name="Name", value=ctx.author.mention, inline=True)
                embed.add_field(name="XP", value=f"{xp}/{int(200 * ((1 / 2) * lvl))}", inline=True)
                embed.add_field(name="Rank", value=f"{rank}/{ctx.guild.member_count}", inline=True)
                embed.add_field(name="Progress Bar", value=boxes * config['completed_bar'] + (20 - boxes) * config['uncompleted_bar'],
                                inline=False)
                embed.add_field(name=f"Level", value=f"{lvl}", inline=False)
                embed.set_thumbnail(url=ctx.message.author.avatar_url)
                await ctx.channel.send(embed=embed)

    @commands.command()
    async def leaderboard(self, ctx):
        if ctx.channel.id == bot_channel:
            rankings = levelling.find().sort("xp", -1)
            i = 1
            con = config['leaderboard_amount']
            embed = discord.Embed(title=f":trophy: Leaderboard | Top {con}")
            for x in rankings:
                try:
                    temp = ctx.guild.get_member(x["id"])
                    tempxp = x["xp"]
                    templvl = x["rank"]
                    embed.add_field(name=f"{i}: {temp.name}", value=f"Level: {templvl} | Total XP: {tempxp}", inline=False)
                    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/809363224663031829/809734218103259146/leaderboards.png")
                    i += 1
                except:
                    pass
                if i == config['leaderboard_amount']:
                    break
            await ctx.channel.send(embed=embed)


def setup(client):
    client.add_cog(levelsys(client))
