import discord
from discord.ext import commands
from ruamel.yaml import YAML
from Systems.levelsys import levelling

# Reads the config file, no need for changing.
yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)


# Spam system class
class background(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def background(self, ctx, link=None):
        await ctx.message.delete()
        if link:
            levelling.update_one({"id": ctx.author.id}, {"$set": {"background": f"{link}"}})
            embed = discord.Embed(title=":white_check_mark: **BACKGROUND CHANGED!**",
                                  description="Your profile background has been set successfully! If your background does not update, please try a new image.")
            embed.set_thumbnail(url=link)
            await ctx.channel.send(embed=embed)
        elif link is None:
            embed3 = discord.Embed(title=":x: **SOMETHING WENT WRONG!**",
                                   description="Please make sure you entered a link.")
            await ctx.channel.send(embed=embed3)


# Sets-up the cog for help
def setup(client):
    client.add_cog(background(client))
