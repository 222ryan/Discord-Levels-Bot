import discord
from discord.ext import commands
from easy_pil import load_image
from ruamel.yaml import YAML

import KumosLab.Database.get
import KumosLab.Database.set

import vacefron



yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)


# Background Class
class background(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Background Command
    @commands.command()
    async def background(self, ctx, url: str = None):
        if url is None:
            embed = discord.Embed(description=f"🔴 **ERROR**: `Incorrect Usage - {config['Prefix']}background <link>`")
            await ctx.send(embed=embed)
            return
        try:
            await ctx.message.delete()

            # This tries to load the image from the url -- if incorrect it will throw an error resulting in the exception below
            load_image(str(url))

            await KumosLab.Database.set.background(user=ctx.author, guild=ctx.guild, link=url)
            embed = discord.Embed(description=f"🟢 **SUCCESS**: `Background Changed To`: [Link]({url})")
            embed.set_thumbnail(url=url)
            await ctx.send(embed=embed)

        except Exception as e:
            embed = discord.Embed(description=f"🔴 **ERROR**: `Invalid Background Link`")
            await ctx.send(embed=embed)
            return


# Sets-up the cog for background
def setup(client):
    client.add_cog(background(client))