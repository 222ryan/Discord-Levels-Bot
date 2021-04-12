import discord
from discord.ext import commands
from ruamel.yaml import YAML
from Systems.levelsys import levelling

# Reads the config file, no need for changing.
yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)

# Spam system class
class fix(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def fix(self, ctx):
        embed = discord.Embed(title=f":white_check_mark: | Fixed User",
                              colour=config['success_embed_colour'])
        msg = await ctx.send(embed=embed)
        counter = 0
        for member in ctx.guild.members:
            counter += 1
            levelling.update_one({"name": f"{member}"}, {"$set": {"guildid": ctx.guild.id}})
            embed = discord.Embed(title=f":white_check_mark: Fixed User | {counter}/{ctx.guild.member_count}",description=f"{member}",
                                  colour=config['success_embed_colour'])
            await msg.edit(embed=embed)
        embed = discord.Embed(title=f":white_check_mark: | Fixed User | {counter}/{ctx.guild.member_count}", description="Fixing has completed.")
        await msg.edit(embed=embed)



# Sets-up the cog for help
def setup(client):
    client.add_cog(fix(client))