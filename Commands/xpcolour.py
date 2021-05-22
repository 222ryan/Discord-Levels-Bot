import discord
from discord.ext import commands
from ruamel.yaml import YAML
from Systems.levelsys import levelling

# Reads the config file, no need for changing.
yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)


# Spam system class
class xpcolour(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def xpcolour(self, ctx, colour=None):
        await ctx.message.delete()
        if colour:
            levelling.update_one({"guildid": ctx.guild.id, "id": ctx.author.id}, {"$set": {"xp_colour": f"{colour}"}})
            prefix = config['Prefix']
            embed = discord.Embed(title=":white_check_mark: **XP COLOUR CHANGED!**",
                                  description=f"Your xp colour has been changed. If you type `{prefix}rank` and nothing appears, try a new hex code. \n**Example**:\n*#0000FF* = *Blue*")
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/812895798496591882/825363205853151252/ML_1.png")
            await ctx.send(embed=embed)
        elif colour is None:
            embed = discord.Embed(title=":x: **SOMETHING WENT WRONG!**",
                                  description="Please make sure you typed a hex code in!.")
            await ctx.send(embed=embed)
            return


# Sets-up the cog for help
def setup(client):
    client.add_cog(xpcolour(client))