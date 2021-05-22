import discord
from discord.ext import commands
from ruamel.yaml import YAML
from Systems.levelsys import levelling

# Reads the config file, no need for changing.
yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)
with open("Configs/spamconfig.yml", "r", encoding="utf-8") as file:
    spamconfig = yaml.load(file)


# Spam system class
class mutetime(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Reset Command
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def mutetime(self, ctx, time=None):
        if spamconfig['antispam_system'] is True:
            stats = levelling.find_one({"server": ctx.guild.id})
            if time is None:
                prefix = config['Prefix']
                embed2 = discord.Embed(title=f":x: SETUP FAILED",
                                       description=f"You need to enter a valid integer!",
                                       colour=config['error_embed_colour'])
                embed2.add_field(name="Example:", value=f"`{prefix}mutetime <seconds>`")
                await ctx.send(embed=embed2)
            elif time:
                levelling.update_one({"server": ctx.guild.id}, {"$set": {"mutedTime": int(time)}})
                embed = discord.Embed(title=f":white_check_mark: MUTED TIME SET!", description=f"Mute Time Now: `{time}s`",
                                      colour=config['success_embed_colour'])
                await ctx.send(embed=embed)



# Sets-up the cog for help
def setup(client):
    client.add_cog(mutetime(client))
