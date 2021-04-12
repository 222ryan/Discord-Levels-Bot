# Imports
import discord
from discord.ext import commands
from ruamel.yaml import YAML
import asyncio

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
        while True:
            await asyncio.sleep(config['clearing'])
            spam = open("Systems/spam.txt", "r+")
            spam.truncate(0)

    # Everytime a user sends a message, it'll will add it to the spam file and after every x seconds it will clear
    @commands.Cog.listener()
    async def on_message(self, ctx):
        counter = 0
        spam = open("Systems/spam.txt", "r+")
        member = ctx.author
        role = discord.utils.get(member.guild.roles, name=config['ignored_role'])
        if role in member.roles:
            return
        if not member.bot:
            for lines in spam:
                if lines.strip("\n") == str(ctx.author.id):
                    counter += 1
            spam.write(f"{str(ctx.author.id)}\n")
        else:
            return

        # Sends a warning message
        if counter == config['messages_for_warning']:
            counter += +1
            embed = discord.Embed(title=f":warning: WARNING",
                                  description=f"<@{ctx.author.id}>, You've been detected for spam. Repeated offences will get you automatically muted! You've been warned. ",
                                  colour=0xFFCC00)
            await ctx.channel.send(embed=embed)
            print(f"User: {ctx.author} has been flagged for spam, we sent them a warning.")

        # If a user ignores the warning, they'll receive a mute
        if counter == config['messages_for_mute'] + 1:
            counter += 0
            member = ctx.author
            rank = discord.utils.get(member.guild.roles, name=config['muted_role'])
            await member.add_roles(rank)  # Adds the muted role
            print(f"User: {ctx.author} failed to follow the warning, they've now been muted.")
            await asyncio.sleep(config['muted_time'])
            await member.remove_roles(rank)  # Removes the muted role when time is up
            print(f"User: {ctx.author} has now been un-muted.")

    # Stats about the antispam system - we do not show when it clears, as this could allow users to bypass this method.
    @commands.command()
    async def antispam(self, ctx):
        embed2 = discord.Embed(title=":warning: Anti-Spam", description="Anti-Spam System ``v1.4``", colour=0xFFCC00)
        embed2.add_field(name="**Mute Time**:", value=f"``{config['muted_time']}s``")
        embed2.add_field(name="**Messages Before Warning**:", value=f"``{config['messages_for_warning']}``")
        embed2.add_field(name="**Messages Before Mute**:", value=f"``{config['messages_for_mute']}``")
        await ctx.channel.send(embed=embed2)


# Sets-up the cog for antispam
def setup(client):
    client.add_cog(spamsys(client))
