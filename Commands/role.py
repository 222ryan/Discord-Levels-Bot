import discord
from discord.ext import commands
from ruamel.yaml import YAML
from Systems.levelsys import levelling

# Reads the config file, no need for changing.
yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)

    roles = []
    level = []
    prefix = config['Prefix']

# Spam system class
class role(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Reset Command
    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def role(self, ctx, addorremove=None, levels=None, *, rolez=None):
        stats = levelling.find_one({"server": ctx.guild.id})
        if stats is None:
            newserver = {"server": ctx.guild.id, f"role": " ", "level": 0}
            levelling.insert_one(newserver)
        if addorremove is None:

            embed2 = discord.Embed(title=f":x: SETUP FAILED",
                                   description=f"You need to define if you want to add or remove a role!",
                                   colour=config['error_embed_colour'])
            embed2.add_field(name="Example:", value=f"`{prefix}role <add|remove> <level> <rolename>`")
            await ctx.send(embed=embed2)
        else:
            if addorremove == "add":
                if levels is None:
                    embed2 = discord.Embed(title=f":x: SETUP FAILED",
                                           description=f"You need to define a level that the user will unlock the role at!",
                                           colour=config['error_embed_colour'])
                    embed2.add_field(name="Example:", value=f"`{prefix}role <add|remove> <level> <rolename>`")
                    await ctx.send(embed=embed2)
                    return
                else:
                    roles.append(str(rolez))
                    if rolez is None:
                        embed2 = discord.Embed(title=f":x: SETUP FAILED",
                                               description=f"You need to define a role the user unlocks!",
                                               colour=config['error_embed_colour'])
                        embed2.add_field(name="Example:", value=f"`{prefix}role <add|remove> <level> <rolename>`")
                        await ctx.send(embed=embed2)
                        return
                    else:
                        level.append(int(levels))

                        levelling.update_one({"server": ctx.guild.id}, {"$set": {f"role": roles, "level": level}})
                        embed = discord.Embed(title=f":white_check_mark: ADDED ROLE!",
                                              description=f"Added Role: `{rolez}` At Level: `{levels}`",
                                              colour=config['success_embed_colour'])
                        await ctx.send(embed=embed)
            elif addorremove == "remove":
                if rolez is None:
                    embed2 = discord.Embed(title=f":x: SETUP FAILED",
                                           description=f"You need to define a role name!",
                                           colour=config['error_embed_colour'])
                    embed2.add_field(name="Example:", value=f"`{prefix}role <add|remove> <levele> <rolename>`")
                    await ctx.send(embed=embed2)
                    return
                else:
                    roles.remove(str(rolez))
                    if levels is None:
                        embed2 = discord.Embed(title=f":x: SETUP FAILED",
                                               description=f"You need to define a level the user unlocks the level!",
                                               colour=config['error_embed_colour'])
                        embed2.add_field(name="Example:", value=f"`{prefix}role <add|remove> <rolename> <level>`")
                        await ctx.send(embed=embed2)
                        return
                    else:
                        level.remove(int(levels))
                        stats = levelling.find_one({"server": ctx.guild.id})
                        levelling.update_one({"server": ctx.guild.id}, {"$set": {"role": roles, "level": level}})
                        await ctx.send(f"{addorremove} and {rolez} and {levels}")
                        embed = discord.Embed(title=f":white_check_mark: REMOVED ROLE",
                                              description=f"Removed Role: `{rolez}` At Level: `{levels}`",
                                              colour=config['success_embed_colour'])
                        await ctx.send(embed=embed)
                return


# Sets-up the cog for help
def setup(client):
    client.add_cog(role(client))