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
    async def fix(self, ctx, type=None):
        counter = 0
        if type is None:
            prefix = config['Prefix']
            embed = discord.Embed(title=f":x: ERROR!",
                                  description=f"You must enter a valid type to fix!\n\n**Example:**\n`{prefix}fix <users|server|kingdoms>`",
                                  colour=config['success_embed_colour'])
            await ctx.send(embed=embed)
            return
        embed = discord.Embed(title=f":white_check_mark: | Fixed User",
                              colour=config['success_embed_colour'])
        msg = await ctx.send(embed=embed)
        if type == "users".lower():
            for member in ctx.guild.members:
                counter += 1
                levelling.update_one({"name": f"{member}", "guildid": ctx.guild.id}, {"$set": {"tag": f"<@{member.id}>", "guildid": ctx.guild.id, "warnings": 0}})
                embed = discord.Embed(title=f":white_check_mark: Fixed User | {counter}/{ctx.guild.member_count}", description=f"{member}",
                                      colour=config['success_embed_colour'])
                await msg.edit(embed=embed)
            embed = discord.Embed(title=f":white_check_mark: | Fixed User | {counter}/{ctx.guild.member_count}", description="Fixing has completed.")
            await msg.edit(embed=embed)
        elif type == "server".lower():
            counter += 1
            levelling.update_one({"server": ctx.guild.id}, {"$set": {"Antispam": False, "mutedRole": "Muted", "mutedTime": 300, "warningMessages": 5, "muteMessages": 6, "ignoredRole": "Ignored"}})
            embed = discord.Embed(title=f":white_check_mark: Fixing Server", description=f"Fixing..",
                                  colour=config['success_embed_colour'])
            await msg.edit(embed=embed)
            embed = discord.Embed(title=f":white_check_mark: | Fixed Server ", description="Fixing has completed.")
            await msg.edit(embed=embed)
        elif type == "kingdoms".lower():
            for member in ctx.guild.members:
                counter += 1
                levelling.update_one({"name": f"{member}", "guildid": ctx.guild.id}, {"$set": {"healPotions": 0, "coins": 0}})
                embed = discord.Embed(title=f":white_check_mark: Fixed User For Kingdoms | {counter}/{ctx.guild.member_count}", description=f"{member}",
                                      colour=config['success_embed_colour'])
                await msg.edit(embed=embed)
            embed = discord.Embed(title=f":white_check_mark: | Fixed Kingdoms | {counter}/{ctx.guild.member_count}", description="Fixing has completed.")
            await msg.edit(embed=embed)




# Sets-up the cog for help
def setup(client):
    client.add_cog(fix(client))