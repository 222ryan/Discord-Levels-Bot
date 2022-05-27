import discord
from discord import File
from easy_pil import Editor, load_image_async, Font, load_image
from ruamel.yaml import YAML
import Commands.rank


import KumosLab.Database.get


yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)
with open("Configs/clan_addon.yml", "r", encoding="utf-8") as file:
    clan_config = yaml.load(file)

def translate(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

async def generate(user: discord.Member = None, guild: discord.Guild = None, clan_Name: str = None):
    if guild is None:
        print("[Custom] Guild is None")
        return
    if user is None:
        print("[Custom] User is None")
        return
    if clan_Name is None:
        print("[Custom] Clan_Name is None")
        return
    try:
        xp = await KumosLab.Database.get.clanXP(clan_Name=clan_Name, guild=guild)
        level = 1

        rank_colour = await KumosLab.Database.get.clanColour(clan_Name=clan_Name, guild=guild)
        clan_owner = await KumosLab.Database.get.clanOwner(clan_Name=clan_Name, guild=guild)

        blur = 0

        while True:
            if xp < ((config['xp_per_level'] / 2 * (level ** 2)) + (config['xp_per_level'] / 2 * level)):
                break
            level += 1
        xp -= ((config['xp_per_level'] / 2 * (level - 1) ** 2) + (config['xp_per_level'] / 2 * (level - 1)))

        next_level_xp = int(config['xp_per_level'] * 2 * ((1 / 2) * level))

        percentage = int((xp / next_level_xp) * 100)

        clan_logo = await KumosLab.Database.get.clanLogo(clan_Name=clan_Name, guild=guild)
        clan_background = clan_config['clan_card_background']

        background_image = load_image(str(clan_background))
        background = Editor(background_image).resize((1280, 720)).blur(amount=int(blur))

        profile_border = load_image(clan_config['clan_icon_border'])
        profile_border = Editor(profile_border).resize((250, 260))

        profile_image = load_image(clan_logo)
        profile = Editor(profile_image).resize((240, 250))


        font_25 = Font.poppins(size=35, variant="bold")
        font_60_bold = Font.poppins(size=60, variant="bold")
        font_40_bold = Font.poppins(size=50, variant="bold")

        background.paste(profile_border, (30, 40))
        background.paste(profile, (35, 45))

        background.text((300, 40), f"{clan_owner}", font=font_60_bold, color=rank_colour)

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



