import discord
from discord.ext import commands
from ruamel.yaml import YAML
from Systems.levelsys import levelling

# Reads the config file, no need for changing.
yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)


# Spam system class
class xppermessage(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Reset Command
    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def xppermessage(self, ctx, xp=None):
        stats = levelling.find_one({"server": ctx.guild.id})
        if stats is None:
            newserver = {"server": ctx.guild.id, "xp_per_message": 10}
            levelling.insert_one(newserver)
        else:
            if xp is None:
                prefix = config['Prefix']
                embed2 = discord.Embed(title=f":x: SETUP FAILED",
                                       description=f"You need to enter the amount of xp!",
                                       colour=config['error_embed_colour'])
                embed2.add_field(name="Example:", value=f"`{prefix}xppermessage <amount>`")
                await ctx.send(embed=embed2)
            elif xp:
                if int(xp) > 100:
                    embed2 = discord.Embed(title=f":x: SETUP FAILED",
                                           description=f"Must be less that `100`! `{xp}` is `{int(xp) - 100}` too much!",
                                           colour=config['error_embed_colour'])
                    await ctx.send(embed=embed2)
                else:
                    levelling.update_one({"server": ctx.guild.id}, {"$set": {"xp_per_message": int(xp)}})
                    embed = discord.Embed(title=f":white_check_mark: XP UPDATED!", description=f"XP Per Message is now: `{xp}`",
                                          colour=config['success_embed_colour'])
                    await ctx.send(embed=embed)


# Sets-up the cog for help
def setup(client):
    client.add_cog(xppermessage(client))
