import discord
from discord.ext import commands
from ruamel.yaml import YAML
import random

import KumosLab.Database.get
import KumosLab.Database.set

yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)


# Blur Class
class blur(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Rank Command
    @commands.command()
    async def setblur(self, ctx, value: int = None):
        if value is None or value < 0 or value > 10:
            embed = discord.Embed(description="🔴 **Error**: `Please enter a value less than or equal to 10.`")
            await ctx.reply(embed=embed)
            return
        try:
            if config['rank_generator'].lower() == "custom":
                member = ctx.author
                await KumosLab.Database.set.blur(user=member, guild=ctx.guild, amount=value)
                embed = discord.Embed(description=f"🟢 **SUCCESS**: `New Blur Value is: {value}`")
                await ctx.reply(embed=embed)
            else:
                return


        except Exception as e:
            print(f"[Blur Command] {e}")



# Sets-up the cog for blur
def setup(client):
    client.add_cog(blur(client))