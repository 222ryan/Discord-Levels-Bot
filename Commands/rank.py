import discord
from discord.ext import commands
from ruamel.yaml import YAML
from Systems.levelsys import levelling
from Systems.levelsys import vac_api

# Reads the config file, no need for changing.
yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)


# Spam system class
class rank(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Rank Command
    @commands.command(aliases=config['rank_alias'])
    async def rank(self, ctx, member=None):
        if member is None:
            user = f"<@!{ctx.author.id}>"
        else:
            user = member
        userget = user.replace('!', '')
        stats = levelling.find_one({"guildid": ctx.message.guild.id, "tag": userget})
        server = levelling.find_one({"guildid": ctx.guild.id})
        if stats is None:
            embed = discord.Embed(description=":x: No Data Found!",
                                  colour=config['error_embed_colour'])
            await ctx.channel.send(embed=embed)
        else:
            xp = stats["xp"]
            lvl = 0
            rank = 0
            while True:
                if xp < ((config['xp_per_level'] / 2 * (lvl ** 2)) + (config['xp_per_level'] / 2 * lvl)):
                    break
                lvl += 1
            xp -= ((config['xp_per_level'] / 2 * (lvl - 1) ** 2) + (config['xp_per_level'] / 2 * (lvl - 1)))
            rankings = levelling.find({"guildid": ctx.guild.id}).sort("xp", -1)
            for x in rankings:
                rank += 1
                if stats["id"] == x["id"]:
                    break
            levelling.update_one({"guildid": ctx.guild.id, "id": ctx.author.id},
                                 {'$set': {"pfp": f"{ctx.author.avatar_url}", "name": f"{ctx.author}"}})
            stats2 = levelling.find_one({"guildid": ctx.message.guild.id, "tag": userget})
            background = stats2["background"]
            circle = stats2["circle"]
            xpcolour = stats2["xp_colour"]
            member = ctx.author.id
            gen_card = await vac_api.rank_card(
                username=str(stats2['name']),
                avatar=stats['pfp'],
                level=int(lvl),
                rank=int(rank),
                current_xp=int(xp),
                next_level_xp=int(config['xp_per_level'] * 2 * ((1 / 2) * lvl)),
                previous_level_xp=0,
                xp_color=str(xpcolour),
                custom_background=str(background),
                is_boosting=bool(member.premium_since),
                circle_avatar=circle
            )
            embed = discord.Embed(colour=config['rank_embed_colour'])
            embed.set_image(url=gen_card.url)
            await ctx.send(embed=embed)


# Sets-up the cog for rank
def setup(client):
    client.add_cog(rank(client))
