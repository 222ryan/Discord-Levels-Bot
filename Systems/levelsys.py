# Version 3.0

# Imports
import discord
from discord.ext import commands
from pymongo import MongoClient
from ruamel.yaml import YAML
import vacefron

# MONGODB SETTINGS *YOU MUST FILL THESE OUT OTHERWISE YOU'LL RUN INTO ISSUES!* - Need Help? Join The Discord Support Server, Found at top of repo.
cluster = MongoClient("mongodb link here - dont forget to insert password and database name!! and remove the <>")
levelling = cluster["databasename here"]["collectionsname here"]

# Reads the config file, no need for changing.
yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)

# Some config options which need to be stored here, again, no need for altering.
bot_channel = config['bot_channel']
talk_channels = config['talk_channels']
level_roles = config['level_roles']
level_roles_num = config['level_roles_num']

# Vac-API, no need for altering!
vac_api = vacefron.Client()


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
                    print(f"User: {message.author.id} has been added to the database! ")
                    levelling.insert_one(newuser)
                else:
                    if config['Prefix'] in message.content:
                        stats = levelling.find_one({"id": message.author.id})
                        xp = stats["xp"]
                        levelling.update_one({"id": message.author.id}, {"$set": {"xp": xp}})
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
                        levelling.update_one({"id": message.author.id}, {"$set": {"rank": + config['xp_per_message']}})
                        embed2 = discord.Embed(title=f":tada: **LEVEL UP!**",
                                               description=f"{message.author.mention} just reached Level: **{lvl}**",
                                               colour=config['embed_colour'])
                        xp = stats["xp"]
                        levelling.update_one({"id": message.author.id}, {"$set": {"rank": lvl, "xp": xp + config['xp_per_message'] * 2}})
                        print(f"User: {message.author} | Leveled UP To: {lvl}")
                        embed2.add_field(name="Next Level:",
                                         value=f"``{int(config['xp_per_level'] * 2 * ((1 / 2) * lvl))}xp``")
                        embed2.set_thumbnail(url=message.author.avatar_url)
                        await message.channel.send(embed=embed2)
                        for i in range(len(level_roles)):
                            if lvl == level_roles_num[i]:
                                await message.author.add_roles(
                                    discord.utils.get(message.author.guild.roles, name=level_roles[i]))
                                embed = discord.Embed(title=":tada: **ROLE UNLOCKED!**",
                                                      description=f"{message.author.mention} has unlocked the **{level_roles[i]}** role!",
                                                      colour=config['embed_colour'])
                                print(f"User: {message.author} | Unlocked Role: {level_roles[i]}")
                                embed.set_thumbnail(url=message.author.avatar_url)
                                await message.channel.send(embed=embed)

# WARNING:: DUE TO AN ISSUE, RANK COMMAND WILL GRANT XP UNTIL A FIX GETS PUT IN PLACE! If you find a working method, please let me know!

    # Rank Command
    @commands.command(aliases=config['rank_alias'])
    async def rank(self, ctx):
        member = ctx.author
        if ctx.channel.id in config['bot_channel']:
            stats = levelling.find_one({"id": ctx.author.id})
            if stats is None:
                embed = discord.Embed(description=":x: You haven't sent any messages!",
                                      colour=config['error_embed_colour'])
                await ctx.channel.send(embed=embed)
            else:
                xp = stats["xp"]
                lvl = 0
                rank = 0
                while True:
                    if xp < ((config['xp_per_level'] / 2 * (lvl ** 2)) + (config['xp_per_level'] / 2 * lvl)):
                        break
                    lvl += 1
                xp -= ((config['xp_per_level'] / 2 * (lvl - 1) ** 2) + (config['xp_per_level'] / 2 * (lvl - 1)))
                boxes = int((xp / (config['xp_per_level'] * 2 * ((1 / 2) * lvl))) * 20)
                rankings = levelling.find().sort("xp", -1)
                for x in rankings:
                    rank += 1
                    if stats["id"] == x["id"]:
                        break
                if config['image_mode'] is False:
                    embed = discord.Embed(title="{}'s Stats Menu | :bar_chart: ".format(ctx.author.name),
                                          colour=config['rank_embed_colour'])
                    embed.add_field(name="Name", value=ctx.author.mention, inline=True)
                    embed.add_field(name="XP",
                                    value=f"{xp}/{int(config['xp_per_level'] * 2 * ((1 / 2) * lvl))}",
                                    inline=True)
                    embed.add_field(name="Rank", value=f"{rank}/{ctx.guild.member_count}", inline=True)
                    embed.add_field(name="Progress Bar",
                                    value=boxes * config['completed_bar'] + (20 - boxes) * config['uncompleted_bar'],
                                    inline=False)
                    embed.add_field(name=f"Level", value=f"{lvl}", inline=False)
                    embed.set_thumbnail(url=ctx.message.author.avatar_url)
                    await ctx.channel.send(embed=embed)
                elif config['image_mode'] is True:
                    gen_card = await vac_api.rank_card(
                        username=str(member),
                        avatar=member.avatar_url_as(format="png"),
                        level=int(lvl),
                        rank=int(rank),
                        current_xp=int(xp),
                        next_level_xp=int(config['xp_per_level'] * 2 * ((1 / 2) * lvl)),
                        previous_level_xp=5,
                        xp_color=str("#ffffff"),
                        custom_background=str(f"{config['background']}"),
                        is_boosting=bool(member.premium_since),
                        circle_avatar=config['circle_picture']
                    )
                    rank_image = discord.File(fp=await gen_card.read(), filename=f"{member.name}_rank.png")
                    await ctx.send(file=rank_image)

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
                    embed.add_field(name=f"{i}: {temp.name}", value=f"Level: {templvl} | Total XP: {tempxp + config['xp_per_message']}", inline=False)
                    embed.set_thumbnail(url=config['leaderboard_image'])
                    i += 1
                except:
                    pass
                if i == config['leaderboard_amount'] + 1:
                    break
            await ctx.channel.send(embed=embed)

    # Reset Command
    @commands.command()
    @commands.has_role(config["admin_role"])
    async def reset(self, ctx, user=None):
        if user:
            userget = user.replace('!', '')
            levelling.update_one({"tag": userget}, {"$set": {"rank": 1, "xp": config['xp_per_message']}})
            embed = discord.Embed(title=f":white_check_mark: RESET USER", description=f"Reset User: {user}",
                                  colour=config['success_embed_colour'])
            print(f"{userget} was reset!")
            await ctx.send(embed=embed)
        else:
            prefix = config['Prefix']
            embed2 = discord.Embed(title=f":x: RESET USER FAILED",
                                   description=f"Couldn't Reset! The User: ``{user}`` doesn't exist or you didn't mention a user!",
                                   colour=config['error_embed_colour'])
            embed2.add_field(name="Example:", value=f"``{prefix}reset`` {ctx.message.author.mention}")
            print("Resetting Failed. A user was either not declared or doesn't exist!")
            await ctx.send(embed=embed2)

    # Help Command
    @commands.command()
    async def help(self, ctx):
        if config['help_command'] is True:
            prefix = config['Prefix']
            top = config['leaderboard_amount']
            xp = config['xp_per_message']

            embed = discord.Embed(title="**HELP PAGE | :book:**",
                                  description=f"Commands & Information. **Prefix**: ``{prefix}``",
                                  colour=config["embed_colour"])
            embed.add_field(name="Leaderboard:", value=f"``{prefix}Leaderboard`` *Shows the Top: **{top}** Users*")
            embed.add_field(name="Rank:", value=f"``{prefix}Rank`` *Shows the Stats Menu for the User*")
            embed.add_field(name="Reset:",
                            value=f"``{prefix}Reset <user>`` *Sets the user back to: ``{config['xp_per_message']}xp`` & Level: ``1``*")
            embed.add_field(name="Other:",
                            value=f"*You will earn ``{xp}xp`` per message | XP Per Level Is: ``{config['xp_per_level']}xp``*")
            embed.set_thumbnail(url=ctx.guild.icon_url)
            await ctx.channel.send(embed=embed)

    @commands.command()
    @commands.has_role(config["admin_role"])
    async def restart(self, ctx):
        await ctx.message.delete()
        print("Restarting.. Hold On!")
        await ctx.bot.logout()


def setup(client):
    client.add_cog(levelsys(client))

# End Of Level System
