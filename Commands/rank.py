import discord
from discord.ext import commands
from ruamel.yaml import YAML

from Systems.levelsys import levelling
from Systems.levelsys import vac_api
# Reads the config file, no need for changing.
from kumoslab.get import getXPColour

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
            stats = levelling.find_one({"guildid": ctx.guild.id, "id": member.id})
            if stats is None:
                embed = discord.Embed(title=":x: No Data Found!",
                                      colour=config['error_embed_colour'])
                await ctx.channel.send(embed=embed)
            else:

                # get the required xp to the next level
                xp = stats["xp"]
                lvl = 0
                rank = 0
                while True:
                    if xp < ((config['xp_per_level'] / 2 * (lvl ** 2)) + (config['xp_per_level'] / 2 * lvl)):
                        break
                    lvl += 1
                xp -= ((config['xp_per_level'] / 2 * (lvl - 1) ** 2) + (config['xp_per_level'] / 2 * (lvl - 1)))

                # gets the users server ranking
                rankings = levelling.find({"guildid": ctx.guild.id}).sort("xp", -1)
                for x in rankings:
                    rank += 1
                    if stats["id"] == x["id"]:
                        break

                gen_card = await vac_api.rank_card(
                    username=str(member),
                    avatar=member.avatar_url,
                    level=int(lvl),
                    rank=int(rank),
                    current_xp=int(xp),
                    next_level_xp=int(config['xp_per_level'] * 2 * ((1 / 2) * lvl)),
                    previous_level_xp=0,
                    xp_color=str(stats["xp_colour"]),
                    custom_background=str(stats["background"]),
                    is_boosting=bool(member.premium_since),
                    circle_avatar=stats["circle"]
                )
                xp_colour = getXPColour(id=member.id, guildID=ctx.guild.id)
                colour_xp = await xp_colour
                without_tag = colour_xp.replace("#", '')
                embed = discord.Embed(colour=int(f"0x{without_tag}", 0))
                embed.set_image(url=gen_card.url)
                await ctx.send(embed=embed)

        except Exception as e:
            print(f"Rank generated an exception.\n\n{e}")


# Sets-up the cog for rank
def setup(client):
    client.add_cog(rank(client))