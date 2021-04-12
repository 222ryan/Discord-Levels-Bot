import discord
from discord.ext import commands
from ruamel.yaml import YAML
from Systems.levelsys import levelling

# Reads the config file, no need for changing.
yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)


# Spam system class
class reset(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Reset Command
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reset(self, ctx, user=None):
        if user:
            userget = user.replace('!', '')
            levelling.delete_one({"guildid": ctx.guild.id, "tag": userget})
            embed = discord.Embed(title=f":white_check_mark: RESET USER", description=f"Reset User: {user}",
                                  colour=config['success_embed_colour'])
            print(f"{userget} was reset!")
            await ctx.send(embed=embed)
        else:
            prefix = config['Prefix']
            embed2 = discord.Embed(title=f":x: RESET USER FAILED",
                                   description=f"Couldn't Reset! The User: `{user}` doesn't exist or you didn't mention a user!",
                                   colour=config['error_embed_colour'])
            embed2.add_field(name="Example:", value=f"`{prefix}reset` {ctx.message.author.mention}")
            print("Resetting Failed. A user was either not declared or doesn't exist!")
            await ctx.send(embed=embed2)


# Sets-up the cog for help
def setup(client):
    client.add_cog(reset(client))