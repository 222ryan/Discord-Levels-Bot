import discord
from discord.ext import commands
from ruamel.yaml import YAML
from Systems.levelsys import levelling
from Systems.levelsys import vac_api

# Reads the config file, no need for changing.
yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)


# Spam system class
class addxp(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Rank Command
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def addxp(self, ctx, xpamount=None, member=None):
        if member is None:
            user = f"<@!{ctx.author.id}>"
        else:
            user = member
        userget = user.replace('!', '')
        stats = levelling.find_one({"guildid": ctx.guild.id, "tag": userget})
        if xpamount:
            xp = stats["xp"]
            levelling.update_one({"guildid": ctx.guild.id, "tag": userget}, {"$set": {"xp": xp + int(xpamount)}})
            embed = discord.Embed(title=":white_check_mark: **ADDED XP!**",
                                  description=f"Added `{xpamount}xp` To: {userget}")
            await ctx.channel.send(embed=embed)
        elif xpamount is None:
            embed3 = discord.Embed(title=":x: **SOMETHING WENT WRONG!**",
                                   description="Please make sure you entered an integer.")
            await ctx.channel.send(embed=embed3)
        return



# Sets-up the cog for rank
def setup(client):
    client.add_cog(addxp(client))
