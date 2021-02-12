import discord
from discord.ext import commands
from pymongo import MongoClient

# Config - More Options in main.py!
bot_channel =  # Channel where bot commands can be sent
talk_channels = []  # Array of channels you can earn XP in

xp_per_message = 5  # How much XP you earn per message

completed_bar = ":blue_square:"  # Customise the completed bar with any emoji
uncompleted_bar = ":white_large_square:"  # Customise the un completed bar with any emoji

level_roles = ['test', 'test2']  # Array of roles you can be rewarded for levelling up
level_roles_num = [1, 2]  # Rank for each role, in same order as level_roles

cluster = MongoClient(
    "mongodb link here - dont forget to insert password and database name!! and remove the <>")

levelling = cluster["databasename here"]["collectionsname here"]

# End of Config


class levelsys(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Online!")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id in talk_channels:
            stats = levelling.find_one({"id": message.author.id})
            if not message.author.bot:
                if stats is None:
                    newuser = {"id": message.author.id, "xp": 0, "rank": 1}
                    levelling.insert_one(newuser)
                else:
                    xp = stats["xp"] + xp_per_message
                    levelling.update_one({"id": message.author.id}, {"$set": {"xp": xp}})
                    lvl = 0
                    while True:
                        if xp < ((50 *(lvl**2))+(50*lvl)):
                            break
                        lvl += 1
                    xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
                    if xp == 0:
                        embed2 = discord.Embed(description=f"{message.author.mention} just reached Level: **{lvl}**")
                        await message.channel.send(f"Well done {message.author.mention}, Level {lvl}")
                        for i in range(len(level_roles)):
                            if lvl == level_roles_num[i]:
                                await message.author.add_roles(
                                    discord.utils.get(message.author.guild.roles, name=level_roles[i]))
                                embed = discord.Embed(
                                    description=f"{message.author.mention} you have unlocked the **{level_roles}** role!")
                                embed.set_thumbnail(url=message.author.avatar_url)
                                await message.channel.send(embed=embed)

    @commands.command()
    async def rank(self, ctx):
        if ctx.channel.id == bot_channel:
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
                xp -= ((50 * (lvl - 1)) + (50 * (lvl - 1)))
                boxes = int((xp / (200 * ((1 / 2) * lvl))) * 20)
                rankings = levelling.find().sort("xp", -1)
                for x in rankings:
                    rank += 1
                    if stats["id"] == x["id"]:
                        break
                embed = discord.Embed(title=f"ctx.author.mention's Level Stats".format(ctx.author.name))
                embed.add_field(name="Name", value=ctx.author.mention, inline=True)
                embed.add_field(name="XP", value=f"{xp}/{int(200 * ((1 / 2) * lvl))}", inline=True)
                embed.add_field(name="Rank", value=f"{rank}/{ctx.guild.member_count}", inline=True)
                embed.add_field(name="Progress Bar", value=boxes * completed_bar + (20 - boxes) * uncompleted_bar,
                                inline=False)
                embed.set_thumbnail(url=ctx.message.author.avatar_url)
                await ctx.channel.send(embed=embed)

    @commands.command()
    async def leaderboard(self, ctx):
        if ctx.channel.id == bot_channel:
            rankings = levelling.find().sort("xp", -1)
            i = 1
            embed = discord.Embed(title="Rankings:")
            for x in rankings:
                try:
                    temp = ctx.guild.get_member(x["id"])
                    tempxp = x["xp"]
                    embed.add_field(name=f"{i}: {temp.name}", value=f"Total XP: {tempxp}", inline=False)
                    i += 1
                except:
                    pass
                if i == 10:
                    break
            await ctx.channel.send(embed=embed)


def setup(client):
    client.add_cog(levelsys(client))
