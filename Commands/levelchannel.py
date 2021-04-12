import discord
from discord.ext import commands
from ruamel.yaml import YAML
from Systems.levelsys import levelling

# Reads the config file, no need for changing.
yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)


# Spam system class
class levelchannel(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Reset Command
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def levelchannel(self, ctx, channel=None):
        stats = levelling.find_one({"server": ctx.guild.id})
        if stats is None:
            newserver = {"server": ctx.guild.id, "level_channel": " "}
            levelling.insert_one(newserver)
        else:
            if channel is None:
                prefix = config['Prefix']
                embed2 = discord.Embed(title=f":x: SETUP FAILED",
                                       description=f"You need to enter a channel name!",
                                       colour=config['error_embed_colour'])
                embed2.add_field(name="Example:", value=f"`{prefix}levelchannel <channelname>`\n\n*** Please do not use the # and enter any -'s! ({prefix}levelchannel test-channel)***")
                await ctx.send(embed=embed2)
            elif channel:
                levelling.update_one({"server": ctx.guild.id}, {"$set": {"level_channel": channel}})
                embed = discord.Embed(title=f":white_check_mark: LEVEL CHANNEL",
                                      description=f"The new level channel is: `{channel}`",
                                      colour=config['success_embed_colour'])
                await ctx.send(embed=embed)


# Sets-up the cog for help
def setup(client):
    client.add_cog(levelchannel(client))
