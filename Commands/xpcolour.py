import discord
from discord.ext import commands
from ruamel.yaml import YAML
import random

import KumosLab.Database.get
import KumosLab.Database.set

yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)


# XP Colour Class
class setcolour(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['setcolor'])
    async def setcolour(self, ctx, hex: str = None):
        if hex is None:
            embed = discord.Embed(
                description=f"🔴 **ERROR**: `Colour Change Failed! - {config['Prefix']}setcolour <#hexcode|random>`")
            await ctx.send(embed=embed)
            return
        try:
            member = ctx.author
            if hex.lower() == "random":
                random_number = random.randint(0, 16777215)
                hex_number = format(random_number, 'x')
                hex_number = '#' + hex_number
                await KumosLab.Database.set.colour(user=member,guild=member.guild, hex=hex_number)
                embed = discord.Embed(description=f"🟢 **SUCCESS**: `Colour Changed to {hex_number}`", color=int(str(hex_number).replace("#", "0x"), 16))
                await ctx.reply(embed=embed)
            else:
                # check if hex includes #
                if hex.startswith("#"):
                    if len(hex) > 7 or len(hex) < 7:
                        embed = discord.Embed(
                            description=f"🔴 **ERROR**: `Colour Change Failed! - Invalid Hex Code`")
                        await ctx.reply(embed=embed)
                    else:
                        await KumosLab.Database.set.colour(user=member,guild=member.guild, hex=hex)
                        embed = discord.Embed(description=f"🟢 **SUCCESS**: `Colour Changed to {hex}`", color=int(str(hex).replace("#", "0x"), 16))
                        await ctx.reply(embed=embed)
                # add # to hex
                else:
                    new_hex = "#" + hex
                    if len(hex) > 7 or len(new_hex) < 7:
                        embed = discord.Embed(
                            description=f"🔴 **ERROR**: `Colour Change Failed! - Invalid Hex Code`")
                        await ctx.reply(embed=embed)
                    else:
                        await KumosLab.Database.set.colour(user=member,guild=member.guild, hex=new_hex)
                        embed = discord.Embed(description=f"🟢 **SUCCESS**: `Colour Changed to {new_hex}`", color=int(str(new_hex).replace("#", "0x"), 16))
                        await ctx.reply(embed=embed)


        except Exception as e:
            print(f"[XP-Colour Command] {e}")

def setup(client):
    client.add_cog(setcolour(client))