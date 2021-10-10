import discord
from discord.ext import commands
from ruamel.yaml import YAML
from Systems.levelsys import levelling

# Reads the config file, no need for changing.
yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)
with open("Configs/spamconfig.yml", "r", encoding="utf-8") as file:
    spamconfig = yaml.load(file)


class talkchannels(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def talkchannel(self, ctx, state=None, channel=None):
        prefix = config['Prefix']
        if state is None:
            embed = discord.Embed(title=":x: SETUP FAILED!", description=f"`You need to define a state! {prefix}talkchannel <add|remove> <channel>`", colour=config['error_embed_colour'])
            await ctx.send(embed=embed)
            return
        if channel is None:
            embed = discord.Embed(title=":x: SETUP FAILED!",
                                  description=f"`You need to define a channel! {prefix}talkchannel <add|remove> <channel>`",
                                  colour=config['error_embed_colour'])
            await ctx.send(embed=embed)
            return
        elif state.lower() == "add":
            channel = discord.utils.get(ctx.guild.channels, name=channel)
            stats = levelling.find_one({"server": ctx.guild.id})
            if stats['ignored_channels'] == "None":
                levelling.update_one({"server": ctx.guild.id}, {"$set": {"ignored_channels": []}})
            levelling.update_one({"server": ctx.guild.id}, {"$push": {"ignored_channels": channel.id}})
            embed = discord.Embed(title="✅ TALK CHANNEL ADDED!", description=f"`You can now earn xp in: {channel.name}`", colour=config['success_embed_colour'])
            await ctx.send(embed=embed)
            return
        elif state.lower() == "remove":
            channel = discord.utils.get(ctx.guild.channels, name=channel)
            levelling.update_one({"server": ctx.guild.id}, {"$pull": {"ignored_channels": channel.id}})
            embed = discord.Embed(title="✅ TALK CHANNEL REMOVED!",
                                  description=f"`You can no longer earn xp in: {channel.name}`",
                                  colour=config['success_embed_colour'])
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
