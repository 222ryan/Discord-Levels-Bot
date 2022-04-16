import discord
from discord.ext import commands
from ruamel.yaml import YAML

import KumosLab.Database.get
import KumosLab.Database.Create.Leaderboard.Local.leaderboard
import KumosLab.Database.Create.Leaderboard.MongoDB.leaderboard



yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)


# leaderboard Class
class leaderboard(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Leaderboard Command
    @commands.command(aliases=config['leaderboard_alias'])
    async def leaderboard(self, ctx, leader_type=None):
        if leader_type == None:
            leader_type = "local"
        else:
            leader_type = leader_type
        if config['Database_Type'].lower() == "local":
            await KumosLab.Database.Create.Leaderboard.Local.leaderboard.leaderboard(self=self, ctx=ctx, guild=ctx.guild, leader_type=leader_type)
        elif config['Database_Type'].lower() == "mongodb":
            await KumosLab.Database.Create.Leaderboard.MongoDB.leaderboard.leaderboard(self=self, ctx=ctx, guild=ctx.guild, leader_type=leader_type)



# Sets-up the cog for leaderboard
def setup(client):
    client.add_cog(leaderboard(client))