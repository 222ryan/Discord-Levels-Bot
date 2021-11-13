import discord
from discord.ext import commands
from ruamel.yaml import YAML
from Systems.levelsys import levelling

# Reads the config file, no need for changing.
yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)


class talkchannels(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def talkchannel(self, ctx, state=None, channel : discord.TextChannel = None):
        prefix = config['Prefix']
        if state == None:
            embed = discord.Embed(description=":x: You need to state if you want to `add` or `remove`")
            await ctx.send(embed=embed)
            return
        if channel is None:
            embed = discord.Embed(description=":x: You need to state a channel")
            await ctx.send(embed=embed)
            return
        if state.lower() == "add":
            stats = levelling.find_one({"server": ctx.guild.id})
            if channel.id in stats['ignored_channels']:
                embed = discord.Embed(description=":x: This channel is already in the list")
                await ctx.send(embed=embed)
                return
            stats['ignored_channels'].append(channel.id)
            levelling.update_one({"server": ctx.guild.id}, {"$set": {"ignored_channels": stats['ignored_channels']}})
            embed = discord.Embed(description=f":white_check_mark: Added {channel.mention} to the Talk List!")
            await ctx.send(embed=embed)
            return
        if state.lower() == "remove":
            stats = levelling.find_one({"server": ctx.guild.id})
            if channel.id not in stats['ignored_channels']:
                embed = discord.Embed(description=":x: This channel is not in the list")
                await ctx.send(embed=embed)
                return
            stats['ignored_channels'].remove(channel.id)
            levelling.update_one({"server": ctx.guild.id}, {"$set": {"ignored_channels": stats['ignored_channels']}})
            embed = discord.Embed(description=f":white_check_mark: Removed {channel.mention} from the Talk List!")
            await ctx.send(embed=embed)
            return
        else:
            embed = discord.Embed(description=":x: You need to state if you want to `add` or `remove`")
            await ctx.send(embed=embed)
            return



    @commands.command()
    @commands.guild_only()
    async def talkchannels(self, ctx):
        stats = levelling.find_one({"server": ctx.guild.id})
        embed = discord.Embed(title="🗣️ // Talk Channels")
        if len(stats['ignored_channels']) > 0:
            embed.add_field(name="Channel List:", value=f"<#{str(stats['ignored_channels']).replace('[', '').replace(']', '').replace(' ', '').replace(',', '>, <#')}>")
        else:
            embed.add_field(name="Channel List:", value=f"`You can talk anywhere!`")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(talkchannels(client))
