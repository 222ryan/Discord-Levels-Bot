import discord
from discord.ext import commands
from ruamel.yaml import YAML
from Systems.levelsys import levelling

# Reads the config file, no need for changing.
yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)

    prefix = config['Prefix']

# Spam system class
class role(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Reset Command
    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def role(self, ctx, addorremove=None, level=None, *, role_name=None):
        if addorremove is None:
            embed = discord.Embed(title=":x: There was an Error!", description=f"`{prefix}role <add|remove> <level> <role>`")
            await ctx.send(embed=embed)
            return
        if level is None:
            embed = discord.Embed(title=":x: There was an Error!", description=f"`{prefix}role <add|remove> <level> <role>`")
            await ctx.send(embed=embed)
            return
        if role_name is None:
            embed = discord.Embed(title=":x: There was an Error!", description=f"`{prefix}role <add|remove> <level> <role>`")
            await ctx.send(embed=embed)
            return
        if addorremove.lower() == "add":
            if level:
                if role_name:
                    levelling.update({"server": ctx.guild.id},
                                     {"$push": {"level": level, "role": role_name}})
                    embed = discord.Embed(title="✅ Role Added!", description=f"Added Role `{role_name}` to be unlocked at Level `{level}`")
                    await ctx.send(embed=embed)
        if addorremove.lower() == "remove":
            if level:
                if role_name:
                    levelling.update({"server": ctx.guild.id},
                                     {"$pull": {"level": level, "role": role_name}})
                    embed = discord.Embed(title="✅ Role Removed!", description=f"Removed Role `{role_name}` from unlocking at Level `{level}`")
                    await ctx.send(embed=embed)


    @commands.command()
    @commands.guild_only()
    async def roles(self, ctx):
        serverstats = levelling.find_one({"server": ctx.guild.id})
        embed = discord.Embed(title="🔓 // LEVEL ROLES", description=f"Level Roles for `{ctx.guild.name}`")
        if len(serverstats['role']) < 1:
            embed.add_field(name="Roles:", value="`There are no roles to unlock!`")
            embed.add_field(name="Level:", value="`No level required!`")
        else:
            embed.add_field(name="Roles:", value=f"`{str(serverstats['role']).replace('[', '').replace(']', '')}`")
            embed.add_field(name="Level:", value=f'`{str(serverstats["level"]).replace("[", "").replace("]", "")}`')
        await ctx.send(embed=embed)


# Sets-up the cog for help
def setup(client):
    client.add_cog(role(client))