import discord
from discord.ext import commands
from ruamel.yaml import YAML

import KumosLab.Database.get
import KumosLab.Database.Create.RankCard.custom
import KumosLab.Database.Create.RankCard.vacefron_gen
import KumosLab.Database.Create.RankCard.text

import vacefron



yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)


# Rank Class
class rank(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Rank Command
    @commands.command(aliases=config['rank_alias'])
    async def rank(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        try:
            if config['rank_generator'].lower() == 'custom':
                rank = await KumosLab.Database.Create.RankCard.custom.generate(user=member, guild=ctx.guild)
                embed = discord.Embed()
                embed.set_image(url="attachment://rank_card.png")
                await ctx.reply(file=rank, embed=embed)
            elif config['rank_generator'].lower() == 'vacefron':
                rank = await KumosLab.Database.Create.RankCard.vacefron_gen.generate(user=member, guild=ctx.guild)
                embed = discord.Embed()
                embed.set_image(url="attachment://rank_card.png")
                await ctx.reply(file=rank, embed=embed)
            elif config['rank_generator'].lower() == 'text':
                rank = await KumosLab.Database.Create.RankCard.text.generate(user=member, guild=ctx.guild)
                await ctx.reply(embed=rank)



        except Exception as e:
            print(f"[Rank Command] {e}")
            embed = discord.Embed(description=":x: **Error**: `User not Found`")
            await ctx.send(embed=embed)
            raise e



# Sets-up the cog for rank
def setup(client):
    client.add_cog(rank(client))