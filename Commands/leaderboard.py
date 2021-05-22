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
    async def leaderboard(self, ctx):
        rankings = levelling.find({"guildid": ctx.guild.id}).sort("xp", -1)
        i = 1
        con = config['leaderboard_amount']
        embed = discord.Embed(title=f":trophy: Leaderboard | Top {con}", colour=config['leaderboard_embed_colour'])
        for x in rankings:
            try:
                temp = ctx.guild.get_member(x["id"])
                tempxp = x["xp"]
                templvl = x["rank"]
                embed.add_field(name=f"#{i}: {temp.name}",
                                value=f"Level: `{templvl}`\nTotal XP: `{tempxp}`\n", inline=True)
                embed.set_thumbnail(url=config['leaderboard_image'])
                i += 1
            except:
                pass
            if i == config['leaderboard_amount'] + 1:
                break
        await ctx.channel.send(embed=embed)


# Sets-up the cog for help
def setup(client):
    client.add_cog(leaderboard(client))