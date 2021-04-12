import asyncio

import discord
from discord.ext import commands
from ruamel.yaml import YAML

# Reads the config file, no need for changing.
yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)


# Spam system class
class help(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Help Command
    @commands.command(aliase="h")
    async def help(self, ctx):
        if config['help_command'] is True:
            prefix = config['Prefix']
            top = config['leaderboard_amount']
            embed = discord.Embed(title=":book: Help Journal | Home",
                                  description=f"Welcome to the Help Journal. My Prefix here is: `{prefix}`\n\nThe Help Journal will give you information on all available commands and any other information.\n\n***REACT BELOW TO SWITCH PAGES*** ")
            embed2 = discord.Embed(title=":book: Help Journal | Rank",
                                   description=f"Command:\n`{prefix}rank or {prefix}rank <@user>`\n\nAbout:\nThe `Rank` command will show the user their current level, server ranking and how much xp you have. Your rank card can be customisable with other commands.\n\n***REACT BELOW TO SWITCH PAGES***")
            embed3 = discord.Embed(title=":book: Help Journal | Leaderboard",
                                   description=f"Command:\n`{prefix}leaderboard`\n\nAbout:\nThe `Leaderboard` command displays the Top {top} users in that server, sorted by XP.\n\n***REACT BELOW TO SWITCH PAGES***")
            embed4 = discord.Embed(title=":book: Help Journal | Background",
                                   description=f"Command:\n`{prefix}background <link>`\n\nAbout:\nThe `Background` command will allow you to change your rank cards background to the image of your choosing.\n\n*Note: Some links may not work! If this is the case, send the image to discord, then copy the media link!*\n\n***REACT BELOW TO SWITCH PAGES***")
            embed5 = discord.Embed(title=":book: Help Journal | Circle Picture",
                                   description=f"Command:\n`{prefix}circlepic <True|False>`\n\nAbout:\nThe `Circlepic` command will allow you to change your rank cards profile picture to be circular if set to `true`.\n\n***REACT BELOW TO SWITCH PAGES***")
            embed6 = discord.Embed(title=":book: Help Journal | XP Colour",
                                   description=f"Command:\n`{prefix}xpcolour <hex code>`\n\nAbout:\nThe `XPColour` command will allow you to change your rank cards xp bar colour to any hex code of your choosing.\n\n***REACT BELOW TO SWITCH PAGES***")
            embed7 = discord.Embed(title=":book: Help Journal | Reset | Admin",
                                   description=f"Command:\n`{prefix}reset <@user>`\n\nAbout:\nThe `Reset` command will allow you to reset any user back to the bottom level. *Admin Only*\n\n***REACT BELOW TO SWITCH PAGES***",
                                   colour=0xc54245)
            embed8 = discord.Embed(title=":book: Help Journal | Fix | Admin",
                                   description=f"Command:\n`{prefix}fix <@user>`\n\nAbout:\nThe `Fix` command will try and fix users database fields when going to a newer version. *Admin Only*\n\n*Note: This may not always work due to certain ways the bot has been built. If so, please do this manually.*\n\n***REACT BELOW TO SWITCH PAGES***",
                                   colour=0xc54245)
            embed9 = discord.Embed(title=":book: Help Journal | LevelChannel | Admin",
                                   description=f"Command:\n`{prefix}levelchannel <channelname>`\n\nAbout:\nThe `Levelchannel` command will let you set the channel where level up messages will send. *Admin Only*\n\n***REACT BELOW TO SWITCH PAGES***",
                                   colour=0xc54245)
            embed10 = discord.Embed(title=":book: Help Journal | DoubleXP | Admin",
                                   description=f"Command:\n`{prefix}doublexp <rolename>`\n\nAbout:\nThe `DoubleXP` command will let you set what role will earn x2 XP *Admin Only*\n\n***REACT BELOW TO SWITCH PAGES***",
                                   colour=0xc54245)
            embed11 = discord.Embed(title=":book: Help Journal | Roles | Admin",
                                   description=f"Command:\n`{prefix}role <add|remove> <level> <rolename>`\n\nAbout:\nThe `Role` command will let you add/remove roles when a user reaches the set level *Admin Only*\n\n***REACT BELOW TO SWITCH PAGES***",
                                   colour=0xc54245)
            contents = [embed, embed2, embed3, embed4, embed5, embed6, embed7, embed8, embed9, embed10, embed11]
            pages = 11
            cur_page = 1
            message = await ctx.send(embed=contents[cur_page - 1])

            await message.add_reaction("◀️")
            await message.add_reaction("▶️")

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]

            while True:
                try:
                    reaction, user = await self.client.wait_for("reaction_add", timeout=30, check=check)

                    if str(reaction.emoji) == "▶️" and cur_page != pages:
                        cur_page += 1
                        await message.edit(embed=contents[cur_page - 1])
                        await message.remove_reaction(reaction, user)

                    elif str(reaction.emoji) == "◀️" and cur_page > 1:
                        cur_page -= 1
                        await message.edit(embed=contents[cur_page - 1])
                        await message.remove_reaction(reaction, user)

                    else:
                        await message.remove_reaction(reaction, user)
                except asyncio.TimeoutError:
                    await message.delete()
                    break




# Sets-up the cog for help
def setup(client):
    client.add_cog(help(client))