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
        xp_colour = await KumosLab.Database.get.colour(user=user, guild=guild)
        background = await KumosLab.Database.get.background(user=user, guild=guild)

        lvl = 0
        rank = 0
        while True:
            if xp < ((config['xp_per_level'] / 2 * (lvl ** 2)) + (config['xp_per_level'] / 2 * lvl)):
                break
            lvl += 1
        xp -= ((config['xp_per_level'] / 2 * (lvl - 1) ** 2) + (config['xp_per_level'] / 2 * (lvl - 1)))

        gen_card = await vac_api.rank_card(
            username=str(user),
            avatar=user.avatar_url,
            level=int(lvl),
            rank=int(user_ranking),
            current_xp=int(xp),
            next_level_xp=int(config['xp_per_level'] * 2 * ((1 / 2) * lvl)),
            previous_level_xp=0,
            xp_color=str(xp_colour),
            custom_background=str(background),
            is_boosting=bool(user.premium_since),
            circle_avatar=False
        )

        card = File(fp=await gen_card.read(), filename="rank_card.png")
        return card



    except Exception as e:
        print(f"[Vacefron Rank Card] {e}")



