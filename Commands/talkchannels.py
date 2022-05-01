import discord
from discord.ext import commands
from ruamel.yaml import YAML

import KumosLab.Database.get
import KumosLab.Database.set
import KumosLab.Database.add

import vacefron

yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)


class talkchannel(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['tc'])
    async def talkchannel(self, ctx, case = None, channel: discord.TextChannel = None):
        if channel is None:
            embed = discord.Embed(description=f"🔴 **ERROR**: `Incorrect Usage - {config['Prefix']}tc <add|remove> <#channel>`")
            await ctx.reply(embed=embed)
            return
        if case is None:
            embed = discord.Embed(description=f"🔴 **ERROR**: `Incorrect Usage - {config['Prefix']}tc <add|remove> <#channel>`")
            await ctx.reply(embed=embed)
            return
        try:
            if case.lower() == "add":
                await KumosLab.Database.add.talkchannel(guild=ctx.guild, channel=channel)
                embed = discord.Embed(
                    description=f"🟢 **SUCCESS**: `💭 Added Talk Channel: {channel}`")
                await ctx.reply(embed=embed)
                return
            elif case.lower() == "remove":
                await KumosLab.Database.remove.talkchannel(guild=ctx.guild, channel=channel)
                embed = discord.Embed(
                    description=f"🟢 **SUCCESS**: `💭 Removed Talk Channel: {channel}`")
                await ctx.reply(embed=embed)
                return
        except Exception as e:
            print(f"[TalkChannel Command] {e}")
            embed = discord.Embed(description=f"🔴 **ERROR**: `Failed to add Talk Channel`")
            await ctx.reply(embed=embed)
            return

    @commands.command(aliases=['tcs'])
    async def talkchannels(self, ctx):
        try:
            channels = await KumosLab.Database.get.talkchannels(guild=ctx.guild)
            if channels is None or len(channels) == 0:
                embed = discord.Embed(description=f"💭: `You can gain XP anywhere!`")
                await ctx.reply(embed=embed)
                return
            else:
                channel_Array = []
                for channel in channels:
                    channel_Array.append(channel)
                if channel_Array[0] is None:
                    embed = discord.Embed(description=f"💭: `You can gain XP anywhere!`")
                    await ctx.reply(embed=embed)
                    return
                # convert channel id to channel object
                channel_List = []
                for x in channel_Array:
                    channel = self.client.get_channel(int(x))
                    channel_List.append(channel.name)
                embed = discord.Embed(description=f"💭: `You can gain XP in:`")
                embed.add_field(name="Talk Channels", value=f"`{channel_List}`".replace("[", "").replace("]", "").replace("'", "").replace(" ", ""))
                await ctx.reply(embed=embed)
                return
        except Exception as e:
            print(f"[TalkChannels Command] {e}")
            embed = discord.Embed(description=f"🔴 **ERROR**: `Failed to get Talk Channels`")
            await ctx.reply(embed=embed)
            return

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        try:
            channels = await KumosLab.Database.get.talkchannels(guild=channel.guild)
            if channel.id in channels:
                await KumosLab.Database.remove.talkchannel(guild=channel.guild, channel=channel)
                return
        except Exception as e:
            print(f"[TalkChannels Command] {e}")
            return



def setup(client):
    client.add_cog(talkchannel(client))
