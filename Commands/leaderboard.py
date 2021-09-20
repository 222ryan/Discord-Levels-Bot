import traceback

import discord
from discord.ext import commands
from ruamel.yaml import YAML
from kumoslab.get import *

# Reads the config file, no need for changing.
from Systems.levelsys import levelling

yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)


# Spam system class
class leaderboard(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Leaderboard Command
    @commands.command(aliases=config['leaderboard_alias'])
    @commands.guild_only()
    async def leaderboard(self, ctx, leader_type=None):
        if leader_type is None:
            rankings = levelling.find({"guildid": ctx.guild.id}).sort("xp", -1)
            con = config['leaderboard_amount']
            embed = discord.Embed(title=f":trophy: {ctx.guild.name}'s Leaderboard | Top {con}", colour=config['leaderboard_embed_colour'])
            i = 1
            for x in rankings:
                try:
                    temp = ctx.guild.get_member(x["id"])
                    tempxp = x["xp"]
                    templvl = x["rank"]
                    xp = "{:,}".format(tempxp)
                    level = "{:,}".format(templvl)
                    embed.add_field(name=f"#{i}: {temp.name}",
                                    value=f"Level: `{level}`\nTotal XP: `{xp}`\n", inline=True)
                    i += 1
                    embed.set_thumbnail(url=ctx.guild.icon_url)
                except:
                    pass
                if i == config['leaderboard_amount'] + 1:
                    break
            await ctx.channel.send(embed=embed)
            return
        if leader_type.lower() == 'global':
            rankings = levelling.find().sort("xp", -1)
            con = config['leaderboard_amount']
            embed = discord.Embed(title=f"🌎 Global Leaderboard | Top {con}", colour=config['leaderboard_embed_colour'])
            i = 1
            for x in rankings:
                try:
                    tempxp = x["xp"]
                    templvl = x["rank"]
                    server = x['guildid']
                    level = "{:,}".format(templvl)
                    guild = self.client.get_guild(server)
                    if str(guild) == 'None':
                        continue
                    xp = "{:,}".format(tempxp)
                    embed.add_field(name=f"#{i}: {x['name']}\n`{guild}`",
                                    value=f"Level: `{level}`\nTotal XP: `{xp}`\n", inline=True)
                    i += 1
                    embed.set_thumbnail(url=ctx.guild.icon_url)
                except:
                    pass
                if i == config['leaderboard_amount'] + 1:
                    break
            await ctx.channel.send(embed=embed)



# Sets-up the cog for help
def setup(client):
    client.add_cog(leaderboard(client))