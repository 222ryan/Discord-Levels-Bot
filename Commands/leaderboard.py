import traceback

import discord
from discord.ext import commands
from ruamel.yaml import YAML

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
    async def leaderboard(self, ctx):
        rankings = levelling.find({"guildid": ctx.guild.id}).sort("xp", -1)
        con = config['leaderboard_amount']
        embed = discord.Embed(title=f":trophy: Leaderboard | Top {con}", colour=config['leaderboard_embed_colour'])
        i = 1
        for x in rankings:
            try:
                temp = ctx.guild.get_member(x["id"])
                tempxp = x["xp"]
                templvl = x["rank"]
                embed.add_field(name=f"#{i}: {temp.name}",
                                value=f"Level: `{templvl}`\nTotal XP: `{tempxp}`\n", inline=True)
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