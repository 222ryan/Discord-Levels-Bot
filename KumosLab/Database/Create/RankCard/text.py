import discord
from discord import File
from easy_pil import Editor, load_image_async, Font, load_image
from ruamel.yaml import YAML
import Commands.rank

import vacefron

import KumosLab.Database.get

vac_api = vacefron.Client()

yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)



async def generate(user: discord.Member = None, guild: discord.Guild = None):
    if guild is None:
        print("[Vacefron] Guild is None")
        return
    if user is None:
        print("[Vacefron] User is None")
        return
    try:

        user_ranking = await KumosLab.Database.get.rankings(user=user, guild=guild)
        lvl = await KumosLab.Database.get.level(user=user, guild=guild)
        xp = await KumosLab.Database.get.xp(user=user, guild=guild)

        lvl = 0
        rank = 0
        while True:
            if xp < ((config['xp_per_level'] / 2 * (lvl ** 2)) + (config['xp_per_level'] / 2 * lvl)):
                break
            lvl += 1
        xp -= ((config['xp_per_level'] / 2 * (lvl - 1) ** 2) + (config['xp_per_level'] / 2 * (lvl - 1)))

        embed = discord.Embed(title=f"👤 {user}' Rank Card")
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="Level:", value=f"{lvl:,}")
        embed.add_field(name="Rank:", value=f"{user_ranking:,}")

        dashes = 10
        max_level = int(config['xp_per_level'] * 2 * ((1 / 2) * lvl))

        # create a progress bar
        dashConvert = int(max_level / dashes)
        currentDashes = int(xp / dashConvert)
        remainingDashes = dashes - currentDashes

        progressDisplay = '🟦' * currentDashes
        remainingDisplay = '⬛' * remainingDashes

        embed.add_field(name=f"Progress ({xp:,} / {max_level:,})", value=f"{progressDisplay}{remainingDisplay}", inline=False)


        return embed



    except Exception as e:
        print(f"[Vacefron Rank Card] {e}")
        raise e



