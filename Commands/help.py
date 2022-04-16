import asyncio

import discord
from discord.ext import commands
from ruamel.yaml import YAML
import KumosLab.Database.get
import KumosLab.Database.set

import os

yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)

# Help Class
class helpcommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx, value: str = None):
        try:
            prefix = config["Prefix"]
            if config['help_command'] is True:
                if value is None:
                    embed = discord.Embed(
                        title=f"{self.client.user.name}'s Command List")
                    embed.set_thumbnail(url=self.client.user.avatar_url)
                    embed.add_field(name="📷 Profile", value=f"`Profile Customisation`")
                    embed.add_field(name="😃 Fun", value=f"`Fun Commands`")
                    if ctx.author.guild_permissions.administrator:
                        embed.add_field(name="🔧 Admin", value=f"`Admin Commands`")
                    if ctx.author.id == int(config["Bot_Owner"]):
                        embed.add_field(name="💼 Owner", value=f"`Owner Commands`")
                    if os.path.isfile("Addons/Extras.py"):
                        embed.add_field(name="🔗 Extras", value=f"`Extra Commands`")

                    msg = await ctx.reply(embed=embed)
                    await msg.add_reaction("📷")
                    await msg.add_reaction("😃")
                    if ctx.author.id == int(config["Bot_Owner"]):
                        await msg.add_reaction("💼")
                    if ctx.author.guild_permissions.administrator:
                        await msg.add_reaction("🔧")
                    if os.path.isfile("Addons/Extras.py"):
                        await msg.add_reaction("🔗")

                    def check(reaction, user):
                        return user == ctx.author and reaction.message.id == msg.id

                    try:
                        reaction, user = await self.client.wait_for('reaction_add', timeout=60.0, check=check)
                        if reaction.emoji == "📷":
                            # remove all reactions
                            await msg.clear_reactions()
                            embed = discord.Embed(title="📷 Profile Commands", description="```background, setblur, setcolour, setborder```")
                            embed.add_field(name="Examples:", value=f"```🖼️ {prefix}background <link> - Changes your Rank Card background\n"
                                                                    f"⚪ {prefix}setcolour <#hex|random> - Sets your XP Bar to the chosen HEX code\n"
                                                                    f"👁️ {prefix}setblur <integer> - Blurs your Rank Cards background\n"
                                                                    f"🖼️ {prefix}setborder <link> - Changes your Rank Cards profile picture border```")
                            await msg.edit(embed=embed)
                        elif reaction.emoji == "🔧":
                            # remove all reactions
                            await msg.clear_reactions()
                            embed = discord.Embed(title="🔧 Admin Commands", description="```role, mainchannel, talkchannel, creator```")
                            embed.add_field(name="Examples:", value=f"```🔨 {prefix}role <add|remove> <@role> <role level> - Adds or removes a role from being unlocked at a certain level\n"
                                                                    f"📢 {prefix}mainchannel <@channel> - Sets the main channel for level up and other sorts\n"
                                                                    f"🗣️ {prefix}talkchannel <add|remove> <@channel> - Adds or removes a channel that allows xp gain\n"
                                                                    f"🔧 {prefix}creator <amount> <role-prefix> - Auto-create roles for the amount and adds to database```")
                            await msg.edit(embed=embed)

                        elif reaction.emoji == "💼":
                            # remove all reactions
                            await msg.clear_reactions()
                            embed = discord.Embed(title="💼 Owner Commands", description="```addon, addons```")
                            embed.add_field(name="Examples:", value=f"```🔨 {prefix}addon <Addon> - Installs an addon\n"
                                                                    f"🔨 {prefix}addons - Lists all installed addons```")
                            await msg.edit(embed=embed)
                        elif reaction.emoji == "😃":
                            # remove all reactions
                            await msg.clear_reactions()
                            embed = discord.Embed(title="😃 Fun Commands", description="```rank, leaderboard, roles, talkchannels```")
                            embed.add_field(name="Examples:", value=f"```🏆 {prefix}rank <@user> - Displays the users Rank Card\n"
                                                                    f"📊 {prefix}leaderboard <local|global> - Displays the rankings of all users in the guild or global\n"
                                                                    f"🔒 {prefix}roles - Displays all the roles you can unlock for levelling up\n"
                                                                    f"🗣️ {prefix}talkchannels - Displays all the channels that allow xp gain```")
                            await msg.edit(embed=embed)
                        elif reaction.emoji == "🔗":
                            # remove all reactions
                            await msg.clear_reactions()
                            embed = discord.Embed(title="🔗 Extras", description="```addxp, removexp```")
                            embed.add_field(name="Examples:", value=f"```🔧 {prefix}addxp <@user> <amount> - Adds XP to a user\n"
                                                f"🔧 {prefix}removexp <@user> <amount> - Removes XP from a user```")
                            await msg.edit(embed=embed)




                    except asyncio.TimeoutError:
                        await msg.delete()


        except Exception as e:
            print(f"[Help Command] {e}")



# Sets-up the cog for help
def setup(client):
    client.add_cog(helpcommand(client))