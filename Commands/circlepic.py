import discord
from discord.ext import commands
from ruamel.yaml import YAML
from Systems.levelsys import levelling

# Reads the config file, no need for changing.
yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)


# Spam system class
class circlepic(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def circlepic(self, ctx, value=None):
        await ctx.message.delete()
        if value == "True":
            levelling.update_one({"guildid": ctx.guild.id, "id": ctx.author.id}, {"$set": {"circle": True}})
            embed1 = discord.Embed(title=":white_check_mark: **PROFILE CHANGED!**",
                                   description="Circle Profile Picture set to: `True`. Set to `False` to return to default.")
            await ctx.channel.send(embed=embed1)
        elif value == "False":
            levelling.update_one({"guildid": ctx.guild.id, "id": ctx.author.id}, {"$set": {"circle": False}})
            embed2 = discord.Embed(title=":white_check_mark: **PROFILE CHANGED!**",
                                   description="Circle Profile Picture set to: `False`. Set to `True` to change it to a circle.")
            await ctx.channel.send(embed=embed2)
        elif value is None:
            embed3 = discord.Embed(title=":x: **SOMETHING WENT WRONG!**",
                                   description="Please make sure you either typed: `True` or `False`.")
            await ctx.channel.send(embed=embed3)


# Sets-up the cog for help
def setup(client):
    client.add_cog(circlepic(client))