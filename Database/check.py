import os
import sqlite3

import discord
from pymongo import MongoClient
from ruamel import yaml\

import numpy as np
from discord import File

from easy_pil import Editor, load_image_async, Font, load_image
import KumosLab.Database.add
import KumosLab.Database.get
import KumosLab.Database.set
import KumosLab.Database.remove

with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)

def translate(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

async def levelUp(user: discord.Member = None, guild: discord.Guild = None):
    if user is None:
        print("Error in 'KumosLab/Database/check.py' - User is None for 'levelUp'")
        return
    if guild is None:
        print("Error in 'KumosLab/Database/check.py' - Guild is None for 'levelUp'")
        return

    try:
        user_xp = await KumosLab.Database.get.xp(user=user, guild=guild)
        lvl = 0

        while True:
            if user_xp < ((config['xp_per_level'] / 2 * (lvl ** 2)) + (config['xp_per_level'] / 2 * lvl)):
                break
            lvl += 1
        user_xp -= ((config['xp_per_level'] / 2 * ((lvl - 1) ** 2)) + (config['xp_per_level'] / 2 * (lvl - 1)))
        if await KumosLab.Database.get.level(user=user, guild=guild) != lvl:
            await KumosLab.Database.set.level(user=user, guild=guild, amount=lvl)

            background_image = load_image(config['level_up_background'])
            background = Editor(background_image).resize((900, 270)).blur(amount=config['level_up_blur'])
            profile_image = load_image(str(user.avatar_url))
            profile = Editor(profile_image).resize((200, 200)).circle_image()

            poppins_big = Font.poppins(variant="bold", size=50)
            poppins_mediam = Font.poppins(variant="bold", size=40)
            poppins_regular = Font.poppins(variant="regular", size=30)

            card_left_shape = [(0, 0), (0, 270), (330, 270), (260, 0)]

            background.polygon(card_left_shape, "#2C2F33")
            border_image = load_image(await KumosLab.Database.get.border(user=user, guild=guild))
            border = Editor(border_image).resize((210, 210)).circle_image()
            background.paste(border, (40, 30))
            background.paste(profile, (45, 35))

            background.text((600, 30), "LEVEL UP!", font=poppins_big, color="white", align="center")
            background.text(
                (600, 80), str(user), font=poppins_regular, color="white", align="center"
            )
            background.text(
                (600, 130), f"LEVEL {lvl:,}", font=poppins_mediam, color="white", align="center"
            )
            background.text(
                (600, 170), f"{translate(user_xp)}/{translate(int(config['xp_per_level'] * 2 * ((1 / 2) * lvl)))} XP",
                font=poppins_regular, color="white", align="center"
            )

            embed = discord.Embed()

            member = user
            if await KumosLab.Database.get.mainChannel(guild=guild) is None:
                channel = guild.system_channel
            else:
                channel = discord.utils.get(member.guild.channels,
                                            name=await KumosLab.Database.get.mainChannel(guild=member.guild))
            if channel is None:
                return
            if config['level_up_ping'] is True:
                await channel.send(f"{user.mention},")

            level_roles = np.asarray(await KumosLab.Database.get.roles(guild=guild))
            level_roles_num = np.asarray(await KumosLab.Database.get.roleLevel(guild=guild))

            for i in range(len(level_roles)):
                if lvl == int(level_roles_num[i]):
                    await user.add_roles(
                        discord.utils.get(user.guild.roles, name=level_roles[i]))
                    background.text(
                        (620, 225),
                        f"ROLE UNLOCKED - {level_roles[i]}".replace("[", "").replace("]", "").replace("'", ''),
                        font=poppins_regular,
                        color="white",
                        align="center",
                    )

                    # remove the previous role
                    if i > 0:
                        await user.remove_roles(
                            discord.utils.get(user.guild.roles, name=level_roles[i - 1]))
                    else:
                        continue

            card = File(fp=background.image_bytes, filename="level_card.png")
            embed.set_image(url="attachment://level_card.png")
            await channel.send(file=card, embed=embed)
    except Exception as e:
        print(f"Error in 'KumosLab/Database/check.py' - {e}")