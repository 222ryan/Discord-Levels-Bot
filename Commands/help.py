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
            home = discord.Embed(title=":book: Help Journal | Home",
                                  description=f"Welcome to the Help Journal. My Prefix here is: `{prefix}`\n\nThe Help Journal will give you information on all available commands and any other information.\n\n***REACT BELOW TO SWITCH PAGES*** ")
            rank = discord.Embed(title=":book: Help Journal | Rank",
                                   description=f"Command:\n`{prefix}rank or {prefix}rank <@user>`\n\nAbout:\nThe `Rank` command will show the user their current level, server ranking and how much xp you have. Your rank card can be customisable with other commands.\n\n***REACT BELOW TO SWITCH PAGES***")
            leaderboard = discord.Embed(title=":book: Help Journal | Leaderboard",
                                   description=f"Command:\n`{prefix}leaderboard`\n\nAbout:\nThe `Leaderboard` command displays the Top {top} users in that server, sorted by XP.\n\n***REACT BELOW TO SWITCH PAGES***")
            background = discord.Embed(title=":book: Help Journal | Background",
                                   description=f"Command:\n`{prefix}background <link>`\n\nAbout:\nThe `Background` command will allow you to change your rank cards background to the image of your choosing.\n\n*Note: Some links may not work! If this is the case, send the image to discord, then copy the media link!*\n\n***REACT BELOW TO SWITCH PAGES***")
            circlepicture = discord.Embed(title=":book: Help Journal | Circle Picture",
                                   description=f"Command:\n`{prefix}circlepic <True|False>`\n\nAbout:\nThe `Circlepic` command will allow you to change your rank cards profile picture to be circular if set to `true`.\n\n***REACT BELOW TO SWITCH PAGES***")
            xpcolour = discord.Embed(title=":book: Help Journal | XP Colour",
                                   description=f"Command:\n`{prefix}xpcolour <hex code>`\n\nAbout:\nThe `XPColour` command will allow you to change your rank cards xp bar colour to any hex code of your choosing.\n\n***REACT BELOW TO SWITCH PAGES***")
            reset = discord.Embed(title=":book: Help Journal | Reset | Admin",
                                   description=f"Command:\n`{prefix}reset <@user>`\n\nAbout:\nThe `Reset` command will allow you to reset any user back to the bottom level. *Admin Only*\n\n***REACT BELOW TO SWITCH PAGES***",
                                   colour=0xc54245)
            fix = discord.Embed(title=":book: Help Journal | Fix | Admin",
                                   description=f"Command:\n`{prefix}fix <users|server|kingdoms>`\n\nAbout:\nThe `Fix` command will try and fix either users, the server you're in or support Kingdoms integration *Admin Only*\n\n*Note: This may not always work due to certain ways the bot has been built. If so, please do this manually.*\n\n***REACT BELOW TO SWITCH PAGES***",
                                   colour=0xc54245)
            levelchannel = discord.Embed(title=":book: Help Journal | LevelChannel | Admin",
                                   description=f"Command:\n`{prefix}levelchannel <channelname>`\n\nAbout:\nThe `Levelchannel` command will let you set the channel where level up messages will send. *Admin Only*\n\n***REACT BELOW TO SWITCH PAGES***",
                                   colour=0xc54245)
            doublexp = discord.Embed(title=":book: Help Journal | DoubleXP | Admin",
                                   description=f"Command:\n`{prefix}doublexp <rolename>`\n\nAbout:\nThe `DoubleXP` command will let you set what role will earn x2 XP *Admin Only*\n\n***REACT BELOW TO SWITCH PAGES***",
                                   colour=0xc54245)
            roles = discord.Embed(title=":book: Help Journal | Roles | Admin",
                                   description=f"Command:\n`{prefix}role <add|remove> <level> <rolename>`\n\nAbout:\nThe `Role` command will let you add/remove roles when a user reaches the set level *Admin Only*\n\n***REACT BELOW TO SWITCH PAGES***",
                                   colour=0xc54245)
            xp = discord.Embed(title=":book: Help Journal | ADD/REMOVE XP | Admin",
                                   description=f"Command:\n`{prefix}<add|remove>xp <amount> <user>`\n\nAbout:\nThe `<add|remove>xp` command will allow you to add or remove xp to a certain user. *Admin Only*\n\n***REACT BELOW TO SWITCH PAGES***",
                                   colour=0xc54245)
            antispamstats = discord.Embed(title=":book: Help Journal | ANTISPAM STATS | Admin",
                               description=f"Command:\n`{prefix}antispamstats`\n\nAbout:\nThe `antispamstats` command will allow you to see the current stats about AntiSpam *Admin Only*\n\n***REACT BELOW TO SWITCH PAGES***",
                               colour=0xc54245)
            antispam = discord.Embed(title=":book: Help Journal | ANTISPAM | Admin",
                               description=f"Command:\n`{prefix}antispam <enable|disable>`\n\nAbout:\nThe `antispam` command will allow you to enable or disable the Anti-Spam system per server. *Admin Only*\n\n***REACT BELOW TO SWITCH PAGES***",
                               colour=0xc54245)
            warningmessages = discord.Embed(title=":book: Help Journal | WARNING MESSAGES | Admin",
                                     description=f"Command:\n`{prefix}warniningmessages <integer>`\n\nAbout:\nThe `warningmessages` command will allow you to set how many messages to receive a warning from Anti-Spam. *Admin Only*\n\n***REACT BELOW TO SWITCH PAGES***",
                                     colour=0xc54245)
            mutemessages = discord.Embed(title=":book: Help Journal | MUTE MESSAGES | Admin",
                                            description=f"Command:\n`{prefix}mutemessages <integer>`\n\nAbout:\nThe `mutemessage` command will allow you to set how many messages to receive a mute from Anti-Spam. *Admin Only*\n\n***REACT BELOW TO SWITCH PAGES***",
                                            colour=0xc54245)
            mutedrole = discord.Embed(title=":book: Help Journal | MUTED ROLE | Admin",
                                         description=f"Command:\n`{prefix}mutedrole <role>`\n\nAbout:\nThe `mutedrole` command will allow you to set what role a muted person receives from Anti-Spam. *Admin Only*\n\n***REACT BELOW TO SWITCH PAGES***",
                                         colour=0xc54245)
            ignoredrole = discord.Embed(title=":book: Help Journal | IGNORED ROLE | Admin",
                                      description=f"Command:\n`{prefix}ignoredrole <role>`\n\nAbout:\nThe `ignoredrole` command will allow you to set a role that gets ignored by Anti-Spam. *Admin Only*\n\n***REACT BELOW TO SWITCH PAGES***",
                                      colour=0xc54245)
            mutetime = discord.Embed(title=":book: Help Journal | MUTE TIME | Admin",
                                        description=f"Command:\n`{prefix}mutetime <seconds>`\n\nAbout:\nThe `mutetime` command will allow you to set how long you get muted for from Anti-Spam. *Admin Only*\n\n***REACT BELOW TO SWITCH PAGES***",
                                        colour=0xc54245)
            contents = [home, rank, leaderboard, background, circlepicture, xpcolour, reset, xp, fix, levelchannel, doublexp, roles, antispamstats, antispam, warningmessages, mutemessages, mutedrole, ignoredrole, mutetime]
            pages = 19
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