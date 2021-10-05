import discord
from discord.ext import commands
from ruamel.yaml import YAML
from Systems.levelsys import levelling


yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)
    
    
class ignoredchannel(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def ignore_channel(self, ctx, channel=None):
        stats = levelling.find_one({"server": ctx.guild.id})
        if stats is None:
            new_server = {"server": ctx.guild.id, "ignored_channel": []}
            levelling.insert_one(new_server)
        else:
            if channel is None:
                prefix = config['Prefix']
                embed2 = discord.Embed(title=f":x: SETUP FAILED",
                                       description=f"You need to enter a channel name!",
                                       colour=config['error_embed_colour'])
                embed2.add_field(name="Example:", value=f"`{prefix}ignored_channel <channel name>`\n\n***"
                                                        f" Please do not use the # and enter any -'s!"
                                                        f" ({prefix}ignored_channel test-channel)***")
                await ctx.send(embed=embed2)
            elif channel:
                channel = discord.utils.get(ctx.guild.channels, name=channel)
                channel_id = channel.id
                levelling.update_one({"server": ctx.guild.id}, {"$push": {"ignored_channel": channel_id}})
                embed = discord.Embed(title=f":white_check_mark: IGNORED CHANNEL",
                                      description=f"Blacklisted channel from XP gaining is: `{channel}`",
                                      colour=config['success_embed_colour'])
                await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def remove_ignore(self, ctx, channel=None):
        if channel is None:
            prefix = config['Prefix']
            embed2 = discord.Embed(title=f":x: SETUP FAILED",
                                   description=f"You need to enter a channel name!",
                                   colour=config['error_embed_colour'])
            embed2.add_field(name="Example:", value=f"`{prefix}remove_ignore <channel name>`\n\n***"
                                                    f" Please do not use the # and enter any -'s!"
                                                    f" ({prefix}remove_ignore test-channel)***")
            await ctx.send(embed=embed2)
        elif channel:
            channel = discord.utils.get(ctx.guild.channels, name=channel)
            channel_id = channel.id
            levelling.update_one({"server": ctx.guild.id}, {"$pull": {"ignored_channel": channel_id}})
            embed = discord.Embed(title=f":white_check_mark: REMOVED CHANNEL FROM IGNORED LIST",
                                  description=f"`{channel}` is removed from xp-blacklisted channel",
                                  colour=config['success_embed_colour'])
            await ctx.send(embed=embed)
        
        
# Sets-up the cog for help
def setup(client):
    client.add_cog(ignoredchannel(client))  
