import discord
from discord import File
from easy_pil import Editor, load_image_async, Font, load_image
from ruamel.yaml import YAML
import Commands.rank


import KumosLab.Database.get


yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)

def translate(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

async def generate(user: discord.Member = None, guild: discord.Guild = None):
    if guild is None:
        print("[Custom] Guild is None")
        return
    if user is None:
        print("[Custom] User is None")
        return
    try:
        xp = await KumosLab.Database.get.xp(user=user, guild=guild)
        level = 1

        rank_colour = await KumosLab.Database.get.colour(user=user, guild=guild)

        blur = await KumosLab.Database.get.blur(user=user, guild=guild)

        while True:
            if xp < ((config['xp_per_level'] / 2 * (level ** 2)) + (config['xp_per_level'] / 2 * level)):
                break
            level += 1
        xp -= ((config['xp_per_level'] / 2 * (level - 1) ** 2) + (config['xp_per_level'] / 2 * (level - 1)))

        next_level_xp = int(config['xp_per_level'] * 2 * ((1 / 2) * level))

        percentage = int((xp / next_level_xp) * 100)

        user_background = await KumosLab.Database.get.background(user=user, guild=guild)
        user_border = await KumosLab.Database.get.border(user=user, guild=guild)

        background_image = load_image(str(user_background))
        background = Editor(background_image).resize((1050, 300)).blur(amount=int(blur))

        user_ranking = await KumosLab.Database.get.rankings(user=user, guild=guild)

        profile_image = load_image(user.avatar_url)
        profile = Editor(profile_image).resize((200, 210))
        border_image = load_image(user_border)
        border = Editor(border_image).resize((210, 220))


        font_25 = Font.poppins(size=35, variant="bold")
        font_60_bold = Font.poppins(size=60, variant="bold")
        font_40_bold = Font.poppins(size=50, variant="bold")

        background.paste(border, (30, 40))
        background.paste(profile, (35, 45))

        if config['name_colour'] is True:
            background.text((260, 40), f"{user}", font=font_60_bold, color=rank_colour)
            background.text(
                (870, 190), f"#{translate(user_ranking)}", font=font_40_bold,
                color=rank_colour
            )
        else:
            background.text((250, 40), f"{user}",
                            font=font_60_bold, color="white")
            background.text(
                (870, 190), f"#{await KumosLab.Database.get.rankings(user=user, guild=user.guild):,}", font=font_40_bold,
                color="white"
            )
        background.text((270, 150), f"Level: {level:,}", font=font_25, color="white")

        background.rectangle((260, 190), width=600, height=40, radius=20)
        if percentage > 5:
            background.bar(
                (260, 190),
                max_width=600,
                height=40,
                percentage=percentage,
                fill=rank_colour,
                radius=20,
            )

        background.text(
            (845, 145), f"{translate(xp)} / {translate(next_level_xp)}", font=font_25, color="white", align="right"
        )

        card = File(fp=background.image_bytes, filename="rank_card.png")
        return card

    except Exception as e:
        print(f"[Custom Rank Card] {e}")
        raise e



