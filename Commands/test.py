
from discord.ext import commands
from ruamel.yaml import YAML
from kumoslab.get import *
from kumoslab.getServer import *
from kumoslab.set import *

yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)


# Spam system class
class test(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Leaderboard Command
    @commands.command()
    @commands.guild_only()
    async def test(self, ctx, member: discord.Member = None):
        # embed
        if member is None:
            member = ctx.author
        xp_colour = getXPColour(id=member.id, guildID=ctx.guild.id)
        colour_xp = await xp_colour
        without_tag = colour_xp.replace("#", '')
        embed = discord.Embed(title=f"TEST | USER | {member.name}", colour=int(f"0x{without_tag}", 0))

        level = getLevel(id=member.id, guildID=ctx.guild.id)
        embed.add_field(name="Level:", value="`" + str(await level) + "`")

        xp = getXP(id=member.id, guildID=ctx.guild.id)
        embed.add_field(name="XP:", value="`" + str(await xp) + "`")

        embed.add_field(name="XP Colour:", value="`" + str(colour_xp) + "`")

        circle = getCirlce(id=member.id, guildID=ctx.guild.id)
        embed.add_field(name="Circle Pic?:", value="`" + str(await circle) + "`")

        background = backgroundUrl(id=member.id, guildID=ctx.guild.id)
        embed.set_image(url=str(await background))

        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def server(self, ctx):
        xp_colour = getXPColour(id=ctx.author.id, guildID=ctx.guild.id)
        colour_xp = await xp_colour
        without_tag = colour_xp.replace("#", '')
        embed = discord.Embed(title=f"TEST | SERVER | {ctx.guild.name}", colour=int(f"0x{without_tag}", 0))
        xp = xpPerMessage(guildID=ctx.guild.id)
        embed.add_field(name="XP/Message:", value='`' + str(await xp) + '`')
        double_xp = doubleXPRole(guildID=ctx.guild.id)
        embed.add_field(name="x2 XP Role:", value='`' + str(await double_xp) + '`')
        level_channel = levelChannel(guildID=ctx.guild.id)
        embed.add_field(name="Level Channel: ", value='`#' + str(await level_channel) + '`')
        levels = getLevels(guildID=ctx.guild.id)
        embed.add_field(name="Levels for Roles:", value='`' + str(await levels) + '`')
        roles = getRoles(guildID=ctx.guild.id)
        embed.add_field(name="Roles for Levels:", value='`' + str(await roles) + '`')
        ignored_role = ignoredRole(guildID=ctx.guild.id)
        embed.add_field(name="Ignored Role:", value='`' + str(await ignored_role) + '`')
        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def setxp(self, ctx, amount=None):
        if amount is None:
            await ctx.send("amount not set")
        await setXP(id=ctx.author.id, guildID=ctx.guild.id, amount=amount)
        await ctx.send(f"Set <@{ctx.author.id}>'s xp to {amount}xp ")

    @commands.command()
    @commands.guild_only()
    async def setbackground(self, ctx, link=None):
        if link is None:
            await ctx.send("amount not set")
        await setBackground(id=ctx.author.id, guildID=ctx.guild.id, link=link)
        await ctx.send(f"Set <@{ctx.author.id}>'s background to {link}")

    @commands.command()
    @commands.guild_only()
    async def setxpcolour(self, ctx, hex_code=None):
        if hex is None:
            await ctx.send("hex not set")
        await setXPColour(id=ctx.author.id, guildID=ctx.guild.id, hex_code=hex_code)
        await ctx.send(f"Set <@{ctx.author.id}>'s xp colour to {hex_code}")

    @commands.command()
    @commands.guild_only()
    async def setcircle(self, ctx, state=None):
        if hex is None:
            await ctx.send("state not set")
        await setCircle(id=ctx.author.id, guildID=ctx.guild.id, value=state)
        await ctx.send(f"Set <@{ctx.author.id}>'s xp colour to {state}")


# Sets-up the cog for help
def setup(client):
    client.add_cog(test(client))
