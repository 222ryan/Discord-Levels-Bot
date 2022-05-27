import discord
import numpy as np
from discord.ext import commands
from ruamel.yaml import YAML

import KumosLab.Database.get
import KumosLab.Database.set
import KumosLab.Database.add
import KumosLab.Database.remove

from discord.ext.commands import RoleNotFound

import vacefron

yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)



# Roles Class
class role(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Role Command
    @commands.command()
    async def role(self, ctx, state: str = None, role_name: discord.Role = None, role_level: int = None):
        if state is None:
            embed = discord.Embed(description=f"🔴 **ERROR**: `You must define add or remove! - {config['Prefix']}role <add|remove> <role> <role level>`")
            await ctx.reply(embed=embed)
            return
        if role is None:
            embed = discord.Embed(description=f"🔴 **ERROR**: `You must define a role! - {config['Prefix']}role <add|remove> <role> <role level>`")
            await ctx.send(embed=embed)
            return
        if role_level is None:
            embed = discord.Embed(description=f"🔴 **ERROR**: `You must define a role level! - {config['Prefix']}role <add|remove> <role> <role level>`")
            await ctx.send(embed=embed)
            return
        try:
            if state.lower() == "add":
                exists = await KumosLab.Database.add.role(guild=ctx.guild, role_name=role_name, role_level=int(role_level))
                if exists == "error":
                    embed = discord.Embed(description=f"🔴 **ERROR**: `Role already exists! - {config['Prefix']}role <add|remove> <role> <role level>`")
                    await ctx.reply(embed=embed)
                    return
                else:
                    embed = discord.Embed(description=f"🟢 **SUCCESS**: `Added {role_name} to unlock at Level {role_level}`")
                    await ctx.reply(embed=embed)
            elif state.lower() == "remove":
                await KumosLab.Database.remove.role(guild=ctx.guild, role_name=role_name, role_level=int(role_level))
                embed = discord.Embed(
                    description=f"🟢 **SUCCESS**: `Removed {role_name} from the Database!`")
                await ctx.reply(embed=embed)

        except RoleNotFound as e:
            embed = discord.Embed(description=f"🔴 **ERROR**: `Role not found! - {config['Prefix']}role <add|remove> <role> <role level>`")
            await ctx.send(embed=embed)
            return

    # Role List Command
    @commands.command()
    async def roles(self, ctx):
        embed = discord.Embed(title="🔓 // LEVEL ROLES", description=f"**Level Roles for** `{ctx.guild.name}`")
        role_array = np.asarray(await KumosLab.Database.get.roles(guild=ctx.guild))
        role_level_array = np.asarray(await KumosLab.Database.get.roleLevel(guild=ctx.guild))
        if role_array is None or role_level_array is None:
            embed.add_field(name="Roles:", value="`There are no roles to unlock!`")
            embed.add_field(name="Level:", value="`No level required!`")
            return
        else:
            embed.add_field(name="Roles:", value=f"`{str(role_array).replace('[', '').replace(']', '')}`")
            embed.add_field(name="Level:", value=f"`{str(role_level_array).replace('[', '').replace(']', '')}`", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def creator(self, ctx, amount: int = None, prefix: str = None):
        if amount is None:
            embed = discord.Embed(description=f"🔴 **ERROR**: `You must define a amount! - {config['Prefix']}creator <amount> <role-prefix>`")
            await ctx.reply(embed=embed)
            return
        if prefix is None:
            embed = discord.Embed(description=f"🔴 **ERROR**: `You must define a role-prefix! - {config['Prefix']}creator <amount> <role-prefix>`")
            await ctx.reply(embed=embed)
            return
        if amount > 50 or amount < 1:
            embed = discord.Embed(description=f"🔴 **ERROR**: `You can only create 50 roles at a time! - {config['Prefix']}creator <amount> <role-prefix>`")
            await ctx.reply(embed=embed)
            return
        if len(prefix) > 10 or len(prefix) < 1:
            embed = discord.Embed(description=f"🔴 **ERROR**: `You can only create a prefix with 10 characters! - {config['Prefix']}creator <amount> <role-prefix>`")
            await ctx.reply(embed=embed)
            return
        # loop amount of times
        message = await ctx.send(f"🔓 **CREATING ROLES**: `Creating {amount} roles with prefix {prefix}. Please wait, this may take some time...`")
        for i in range(amount):
            # create role
            role = await ctx.guild.create_role(name=f"{prefix} {i + 1}")
            # add role to database
            await KumosLab.Database.add.role(guild=ctx.guild, role_name=role, role_level=i + 1)

        await message.edit(content=f"🔓 **CREATING ROLES**: `Created {amount} roles with prefix {prefix}.`")











# Sets-up the cog for roles
def setup(client):
    client.add_cog(role(client))
