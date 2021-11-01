import asyncio

import discord
from discord.ext import commands
from ruamel.yaml import YAML
from Systems.levelsys import levelling
import psutil

yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)


# Spam system class
class Stats(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def monitor(self, ctx):
        bot_stats = levelling.find_one({"bot_name": f"{self.client.user.name}"})
        embed = discord.Embed(title="📈  // MONITOR STATS", description=f"`Monitoring {self.client.user.name}`")
        embed.add_field(name="Ping:", value=f"`{round(self.client.latency * 1000)}ms`")
        embed.add_field(name="CPU:", value=f"`{psutil.cpu_percent()}%`")
        embed.add_field(name="Memory:", value=f"`{psutil.virtual_memory()[2]}%`")
        embed.add_field(name="Servers:", value=f"`{len(list(self.client.guilds))}`")
        embed.add_field(name="Members:", value=f"`{len(list(self.client.users))}`")
        embed.add_field(name="Messages:", value=f"`{bot_stats['total_messages'] - 1}`")
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if not ctx.author.bot:
            bot_stats = levelling.find_one({"bot_name": f"{self.client.user.name}"})
            check_field = levelling.find({"total_messages": {"$exists": False}})
            if check_field is None:
                levelling.update_one({"bot_name": f"{self.client.user.name}"}, {"$set": {"total_messages": 1}})
            else:
                messages = bot_stats['total_messages'] + 1
                levelling.update_one({"bot_name": f"{self.client.user.name}"}, {"$set": {"total_messages": messages}})



# Sets-up the cog for Profile+
def setup(client):
    client.add_cog(Stats(client))
