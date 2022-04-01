import discord
from discord.ext import commands
from easy_pil import load_image
from ruamel.yaml import YAML
import random

import KumosLab.Database.get
import KumosLab.Database.set

yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)


class border(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def setborder(self, ctx, url: str = None):
        if url is None:
            embed = discord.Embed(
                description=f"🔴 **ERROR**: `Incorrect Usage! - {config['Prefix']}setborder <link>`")
            await ctx.send(embed=embed)
            return
        try:
            await ctx.message.delete()

            # This tries to load the image from the url -- if incorrect it will throw an error resulting in the exception below
            load_image(str(url))

            await KumosLab.Database.set.border(user=ctx.author, guild=ctx.guild, link=url)
            embed = discord.Embed(description=f"🟢 **SUCCESS**: `Border Changed To`: [Link]({url})")
            embed.set_thumbnail(url=url)
            await ctx.send(embed=embed)

        except Exception as e:
            embed = discord.Embed(
                description=f"🔴 **ERROR**: `Invalid Link! - {config['Prefix']}setborder <link>`")
            await ctx.send(embed=embed)
            return


def setup(client):
    client.add_cog(border(client))
