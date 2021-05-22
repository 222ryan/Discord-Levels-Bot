# Imports
import discord
from discord.ext import commands
from ruamel.yaml import YAML
import asyncio
from Systems.levelsys import levelling
import atexit

# Reads the config file, no need for changing.
yaml = YAML()
with open("Configs/spamconfig.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)


# Spam system class
class spamsys(commands.Cog):
    def __init__(self, client):
        self.client = client

    # On Start, the spam file will be cleared every x seconds (set in spamconfig)
    @commands.Cog.listener()
    async def on_ready(self):
        print("Started System: AntiSpam")
        print("------")

    # Everytime a user sends a message, it'll will add it to the spam file and after every x seconds it will clear
    @commands.Cog.listener()
    async def on_message(self, ctx):
        counter = 0
        serverstats = levelling.find_one({"server": ctx.guild.id})
        stats = levelling.find_one({"guildid": ctx.guild.id, "id": ctx.author.id})
        if serverstats['Antispam'] is True:
            member = ctx.author
            role = discord.utils.get(member.guild.roles, name=serverstats['ignoredRole'])
            if role in member.roles:
                return
            warningmessage = serverstats['warningMessages']
            mutemessage = serverstats['muteMessages']
            if not member.bot:
                counter += 1
                warnings = stats['warnings']
                levelling.update_one({"guildid": ctx.guild.id, "id": ctx.author.id}, {"$set": {"warnings": warnings + 1}})
            else:
                return

            # Sends a warning message
            if warnings == warningmessage - 1:
                embed = discord.Embed(title=f":warning: WARNING",
                                      description=f"<@{ctx.author.id}>, You've been detected for spam. Repeated offences will get you automatically muted! You've been warned. ",
                                      colour=0xFFCC00)
                await ctx.channel.send(embed=embed)
                print(f"User: {ctx.author} has been flagged for spam, we sent them a warning.")

            # If a user ignores the warning, they'll receive a mute
            if warnings == mutemessage - 1:
                takeaway = serverstats['xp_per_message'] * serverstats['muteMessages']
                xp = stats['xp'] - takeaway
                member = ctx.author
                rank = discord.utils.get(member.guild.roles, name=serverstats['mutedRole'])
                await member.add_roles(rank)  # Adds the muted role
                print(f"User: {ctx.author} failed to follow the warning, they've now been muted.")
                await asyncio.sleep(serverstats['mutedTime'])
                await member.remove_roles(rank)  # Removes the muted role when time is up
                print(f"User: {ctx.author} has now been un-muted.")
                levelling.update_one({"guildid": ctx.guild.id, "id": ctx.author.id}, {"$set": {"warnings": 0}})
                levelling.update_one({"guildid": ctx.guild.id, "id": ctx.author.id},
                                     {"$set": {"xp": xp}})

        while True:
            await asyncio.sleep(config['clearing'])
            levelling.update_one({"guildid": ctx.guild.id, "id": ctx.author.id},
                                 {"$set": {"warnings": 0}})

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def antispamstats(self, ctx):
        serverstats = levelling.find_one({"server": ctx.guild.id})
        embed2 = discord.Embed(title=":warning: Anti-Spam", description="Anti-Spam System `v1.5`", colour=0xFFCC00)
        embed2.add_field(name="**Mute Time**:", value=f"`{serverstats['mutedTime']}s`")
        embed2.add_field(name="**Messages Before Warning**:", value=f"`{serverstats['warningMessages']}`")
        embed2.add_field(name="**Messages Before Mute**:", value=f"`{serverstats['muteMessages']}`")
        if serverstats['Antispam'] is True:
            embed2.add_field(name="**Status**:", value=f"`Enabled`")
        else:
            embed2.add_field(name="**Status**:", value=f"`Disabled`")
        await ctx.channel.send(embed=embed2)

    @commands.Cog.listener()
    async def exit_handler(self, ctx):
        serverstats = levelling.find_one({"server": ctx.guild.id})
        for member in ctx.guild.members:
            user = ctx.author
            role = discord.utils.get(ctx.guild.roles, name=serverstats["mutedRole"])
            if role in user.roles:
                await member.remove_roles(role)



# Sets-up the cog for antispam
def setup(client):
    client.add_cog(spamsys(client))
