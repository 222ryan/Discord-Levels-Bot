import os
import discord
import ruamel.yaml
from ruamel import yaml
from discord.ext import commands
import KumosLab.Database.add
import KumosLab.Database.remove
import KumosLab.Database.check

with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)

class Extras(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("[Extras Addon] Addon Started - Add or Remove XP from users!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def addxp(self, ctx, user: discord.Member = None, xp: int = None):
        if user is None:
            embed = discord.Embed(description="🔴 **ERROR**: `No user specified`")
            await ctx.reply(embed=embed)
            return
        if xp is None or xp <= 0:
            embed = discord.Embed(description="🔴 **ERROR**: `No amount specified`")
            await ctx.reply(embed=embed)
            return
        try:
            await KumosLab.Database.add.xp(user=user, guild=ctx.guild, amount=xp)
            await KumosLab.Database.check.levelUp(user=user, guild=ctx.guild)
            embed = discord.Embed(description=f"🟢 **SUCCESS**: `Added {xp}xp to {user}`")
            await ctx.reply(embed=embed)
        

        except Exception as e:
            print(f"[Extras Addon] {e}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def removexp(self, ctx, user: discord.Member = None, xp: int = None):
        if user is None:
            embed = discord.Embed(description="🔴 **ERROR**: `No user specified`")
            await ctx.reply(embed=embed)
            return
        if xp is None or xp <= 0:
            embed = discord.Embed(description="🔴 **ERROR**: `No amount specified`")
            await ctx.reply(embed=embed)
            return
        try:
            await KumosLab.Database.remove.xp(user=user, guild=ctx.guild, amount=xp)
            await KumosLab.Database.check.levelUp(user=user, guild=ctx.guild)
            embed = discord.Embed(description=f"🟢 **SUCCESS**: `Removed {xp}xp from {user}`")
            await ctx.reply(embed=embed)

        except Exception as e:
            print(f"[Extras Addon] {e}")



def setup(client):
    client.add_cog(Extras(client))
