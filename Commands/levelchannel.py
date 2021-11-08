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
    @commands.guild_only()
    async def levelchannel(self, ctx, channel: discord.TextChannel = None):
        stats = levelling.find_one({"server": ctx.guild.id})
        if stats is None:
            newserver = {"server": ctx.guild.id, "level_channel": " "}
            levelling.insert_one(newserver)

        if channel is None:
            embed = discord.Embed(description=":x: You must mention a channel!")
            await ctx.send(embed=embed)
            return
        else:
            levelling.update_one({"server": ctx.guild.id}, {"$set": {"level_channel": channel.name}})
            embed = discord.Embed(description=f":white_check_mark: Level channel set to {channel}")
            await ctx.send(embed=embed)



# Sets-up the cog for help
def setup(client):
    client.add_cog(levelchannel(client))
