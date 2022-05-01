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




# MainChannel Class
class mainchannel(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Rank Command
    @commands.command(aliases=['mc'])
    async def mainchannel(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            if await KumosLab.Database.get.mainChannel(guild=ctx.guild) is None:
                embed = discord.Embed(description=f"🔴 **ERROR**: `Incorrect Usage - {config['Prefix']}mc <#channel>`")
                await ctx.reply(embed=embed)
                return
        try:
            await KumosLab.Database.set.mainChannel(guild=ctx.guild, channel=channel)
            embed = discord.Embed(
                description=f"🟢 **SUCCESS**: `📢 Main Channel set to: {await KumosLab.Database.get.mainChannel(guild=ctx.guild)}`")
            await ctx.reply(embed=embed)
        except Exception as e:
            print(f"[MainChannel Command] {e}")
            embed = discord.Embed(description=f"🔴 **ERROR**: `Failed to set Main Channel`")
            await ctx.reply(embed=embed)
            return

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        try:
            channels = await KumosLab.Database.get.mainChannel(guild=channel.guild)
            if channel.id in channels:
                # get random channel in guild
                channel = await channel.guild.fetch_channels()
                channel = channel[0]
                await KumosLab.Database.set.mainChannel(guild=channel.guild, channel=None)
                return
        except Exception as e:
            print(f"[MainChannel Command] {e}")
            return







# Sets-up the cog for mainchannel
def setup(client):
    client.add_cog(mainchannel(client))
