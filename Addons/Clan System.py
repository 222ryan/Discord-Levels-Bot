import asyncio
import re

import discord
from discord.ext import commands
from ruamel.yaml import YAML
from Systems.levelsys import levelling

# Reads the config file, no need for changing.
yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)


# Spam system class
class Clan(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def clan(self, ctx, state=None):
        prefix = config['Prefix']
        if state is None:
            embed = discord.Embed(title="👑 | CLAN SYSTEM", description="Welcome to the Clan System. Invite friends to earn xp simultaneously when someone from the same clan sends a message.")
            embed.add_field(name="Usages:", value=f"`{prefix}create <clanName>` - Allows you to create a clan. Requires Level:  `{config['level_for_clan']}`\n`{prefix}invite <user>` - Invites a user to your clan (If private)\n`{prefix}join <clanName>` - Joins a clan (If public)")
            embed.add_field(name="How to view clan info?", value=f"{prefix}clan <clanName>")
            await ctx.send(embed=embed)
            return
        if state:
            clan_search = levelling.find_one({"guildid": ctx.guild.id, "clan_name": state})
            if clan_search:
                members = str(clan_search['users']).replace("'", "").replace("[", "").replace("]", "")
                embed = discord.Embed(title=f"{state.upper()} CLAN | {str(clan_search['status']).upper()}")
                embed.add_field(name=f"Owner:", value=f"<@{clan_search['owner']}>")
                embed.add_field(name=f"Member Count:", value=f"`{len(clan_search['users'])}/10`")
                embed.add_field(name="XP Earned:", value=f"`{clan_search['total_xp']}`")
                embed.add_field(name="Members:", value=f"```{members}```")
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title=":x: There was an Error!",
                                      description=f"The clan `{state}` does not exist. Did you make a typo?")
                await ctx.send(embed=embed)




    @commands.command()
    async def create(self, ctx, name=None, publicity=None):
        owner = ctx.author
        if name is None:
            embed = discord.Embed(title=":x: There was an Error!", description="*You need to define a name for the clan!*")
            await ctx.send(embed=embed)
            return
        if publicity is None:
            embed = discord.Embed(title=":x: There was an Error!",
                                  description="*You need to define if the clan is `private` or `public`!*")
            await ctx.send(embed=embed)
            return
        if publicity.lower() != 'public' and publicity.lower() != 'private':
            embed = discord.Embed(title=":x: There was an Error!",
                                  description="*You need to define if the clan is `private` or `public`!*")
            await ctx.send(embed=embed)
            return
        elif name:
            clan_search = levelling.find_one({"guildid": ctx.guild.id, "clan_name": name})
            user_search = levelling.find_one({"guildid": ctx.guild.id, "owner": ctx.author.id})
            user_in_clan_search = levelling.find_one({"guildid": ctx.guild.id, "users": f"{ctx.author}"})
            stats = levelling.find_one({"guildid": ctx.guild.id, "name": f"{owner}"})
            level = stats['rank']
            if user_search:
                embed = discord.Embed(title=":x: There was an Error!", description="`You already own a clan!`")
                await ctx.send(embed=embed)
                return
            if user_in_clan_search:
                embed = discord.Embed(title=":x: There was an Error!", description="`You are already in a clan!`")
                await ctx.send(embed=embed)
                return
            if int(level) < int(config['level_for_clan']):
                embed = discord.Embed(title=":x: There was an error!", description=f"*You aren't the right level to create a clan! Level up `{config['level_for_clan']-level}` times!*")
                await ctx.send(embed=embed)
                return
            if clan_search:
                embed = discord.Embed(title=":x: There was an error!", description=f"The clan `{name}` already exists!")
                await ctx.send(embed=embed)
                return
            else:
                newclan = {"guildid": ctx.guild.id, "clan_name": name.lower(), "owner": ctx.author.id, "users": [f'{ctx.author}'],
                           "status": publicity.lower(), "total_xp": 0}
                levelling.insert_one(newclan)
                embed = discord.Embed(title=f"{name.upper()} CLAN", description=f"You have successfully created a clan with the name `{name.lower()}`!")
                embed.add_field(name=f"Owner:", value=f"{owner.mention}")
                embed.add_field(name="Members:", value=f"{owner.name}")
                embed.add_field(name="Status:", value=f"`{publicity.upper()}`")
                embed.add_field(name="XP Earned:", value=f"`0xp`")
                embed.add_field(name=f"Member Count:", value="`1/10`")
                await ctx.send(embed=embed)



    @commands.command()
    async def invite(self, ctx, member: discord.Member = None):
        prefix = config['Prefix']
        clan_search = levelling.find_one({"guildid": ctx.guild.id, "owner": ctx.author.id})
        if member is None:
            embed = discord.Embed(title=":x: There was an Error!", description="`You need to define a user to invite!`")
            await ctx.send(embed=embed)
            return
        if member == ctx.author:
            embed = discord.Embed(title=":x: There was an Error!",
                                  description=f"`You cannot invite yourself!`")
            await ctx.send(embed=embed)
            return
        if len(clan_search['users']) >= 10:
            embed = discord.Embed(title=":x: There was an Error!",
                                  description=f"`The clan {clan_search['clan_name']} is full!`")
            await ctx.send(embed=embed)
            return
        status = clan_search['status']
        if status == 'public':
            embed = discord.Embed(title=":x: There was an Error!",
                                  description=f"`This clan is Public. {member.mention} should use: `{prefix}join {clan_search['clan_name']}` instead.")
            await ctx.send(embed=embed)
            return
        if member:
            embed = discord.Embed(title=f"CLAN INVITE | {clan_search['clan_name']}", description=f"You have received an invitation from {ctx.author.mention} to join `{clan_search['clan_name']}`")
            embed.add_field(name="How to Join?", value="React With ✅ to Accept.\nReact With :x: to Decline.")
            embed.set_footer(text=f"This invitation was sent from {ctx.author} from {ctx.guild.name}")
            message = await member.send(embed=embed)
            embed = discord.Embed(description=f"Invite sent to `{member.name}`! They have `5` Minutes to Accept.")
            await ctx.send(embed=embed)

            await message.add_reaction(f"✅")
            await message.add_reaction("❌")

            def check(reaction, user):
                return user == member and str(reaction.emoji) in [f"✅","❌"]

            while True:
                try:
                    reaction, user = await self.client.wait_for("reaction_add", timeout=300, check=check)
                    if str(reaction.emoji) == f"❌":
                        embed = discord.Embed(description=f"{ctx.author.mention}, {member.mention} declined your clan invite to `{clan_search['clan_name']}`")
                        await ctx.author.send(embed=embed)
                        return
                    if str(reaction.emoji) == "✅":
                        user_search = levelling.find_one({"guildid": ctx.guild.id, "users": f"{member}"})
                        if user_search:
                            embed = discord.Embed(title=":x: There was an Error!",
                                                  description="`You are already in a clan!`")
                            await member.send(embed=embed)
                            embed = discord.Embed(
                                description=f"{ctx.author.mention}, {member.mention} failed to join your clan as they are already in one!")
                            await ctx.author.send(embed=embed)
                            return
                        embed = discord.Embed(
                            description=f"{ctx.author.mention}, {member.mention} accepted your clan invite to `{clan_search['clan_name']}`")
                        await ctx.author.send(embed=embed)
                        levelling.update({"guildid": ctx.guild.id, "clan_name": clan_search['clan_name']},
                                         {"$push": {"users": f'{member}'}})
                        return
                    else:
                        await message.remove_reaction(reaction, user)
                except asyncio.TimeoutError:
                    await message.delete()
                    embed = discord.Embed(
                        description=f"{ctx.author.mention}, {member.mention} didn't respond in time.")
                    await ctx.send(embed=embed)
                    break

    @commands.command()
    async def join(self, ctx, clan=None):
        if clan is None:
            embed = discord.Embed(title=":x: There was an Error!", description="`You need to specify which clan to join!`")
            await ctx.send(embed=embed)
        elif clan:
            clan_search = levelling.find_one({"guildid": ctx.guild.id, "clan_name": clan})
            user_search = levelling.find_one({"guildid": ctx.guild.id, "users": f"{ctx.author}"})
            if user_search:
                if str(ctx.author) in user_search['users']:
                    embed = discord.Embed(title=":x: There was an Error!", description="`You are already in a clan!`")
                    await ctx.send(embed=embed)
                    return
            else:
                if clan_search:
                    if len(clan_search['users']) >= 10:
                        embed = discord.Embed(title=":x: There was an Error!", description=f"The clan `{clan}` is full!")
                        await ctx.send(embed=embed)
                        return
                    if clan_search['status'] == "private":
                        embed = discord.Embed(title=":x: There was an Error!", description=f"The clan `{clan}` is `private`!")
                        await ctx.send(embed=embed)
                        return
                    else:
                        levelling.update({"guildid": ctx.guild.id, "clan_name": clan_search['clan_name']},
                                         {"$push": {"users": f"{ctx.author}"}})
                        embed = discord.Embed(title=f":white_check_mark: You joined the clan `{clan_search['clan_name']}`!")
                        await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title=":x: There was an Error", description=f"The clan `{clan}` does not exist!")
                    await ctx.send(embed=embed)

    @commands.command()
    async def status(self, ctx):
        clan_search = levelling.find_one({"guildid": ctx.guild.id, "owner": ctx.author.id})
        if clan_search['status'] == "private":
            levelling.update_one({"guildid": ctx.guild.id, "owner": ctx.author.id}, {"$set": {"status": "public"}})
            embed = discord.Embed(title=f":white_check_mark: Status for `{clan_search['clan_name']}` set to `Public`")
            await ctx.send(embed=embed)
        else:
            levelling.update_one({"guildid": ctx.guild.id, "owner": ctx.author.id}, {"$set": {"status": "private"}})
            embed = discord.Embed(title=f":white_check_mark: Status for `{clan_search['clan_name']}` set to `Private`")
            await ctx.send(embed=embed)

    @commands.command()
    async def delete(self, ctx):
        clan_search = levelling.find_one({"guildid": ctx.guild.id, "owner": ctx.author.id})
        if clan_search:
            levelling.delete_one({"guildid": ctx.guild.id, "owner": ctx.author.id})
            embed = discord.Embed(title=f":white_check_mark: The clan `{clan_search['clan_name']}` was successfully deleted!")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=":x: There was an Error", description="You do not own a clan!")
            await ctx.send(embed=embed)

    @commands.command()
    async def leave(self, ctx):
        user_in_clan_search = levelling.find_one({"guildid": ctx.guild.id, "users": f"{ctx.author}"})
        clan_search = levelling.find_one({"guildid": ctx.guild.id, "clan_name": user_in_clan_search['clan_name']})
        if clan_search:
            if ctx.author.id == clan_search['owner']:
                embed = discord.Embed(title=":x: There was an Error!", description="`You are the owner of the clan, you must delete it to leave!`")
                await ctx.send(embed=embed)
                return
            levelling.update({"guildid": ctx.guild.id, "clan_name": clan_search['clan_name']},
                             {"$pull": {"users": f"{ctx.author}"}})
            embed = discord.Embed(title=f":white_check_mark: You have left the clan `{clan_search['clan_name']}`")
            await ctx.send(embed=embed)

    @commands.command()
    async def clans(self, ctx):
        clan_search = levelling.find_one({"guildid": ctx.guild.id, "status": "public"})
        if clan_search:
            rankings = levelling.find({"guildid": ctx.guild.id, "status": "public"}).sort(str(len(clan_search['users'])), -1)
            embed = discord.Embed(title=f":video_game: PUBLIC CLANS | `10 RESULTS`",
                                  colour=config['leaderboard_embed_colour'])
            i = 1
            for x in rankings:
                try:
                    members = x["users"]
                    name = x["clan_name"]
                    xp = x["total_xp"]
                    embed.add_field(name=f"#{i}: {name}",
                                    value=f"Members: `{len(members)}`\nXP Earned: `{xp}xp`", inline=True)
                    i += 1
                    embed.set_thumbnail(url=ctx.guild.icon_url)
                except:
                    pass
                if i == 11:
                    break
            await ctx.channel.send(embed=embed)
        else:
            embed = discord.Embed(title=":video_game: PUBLIC CLANS | `NO RESULTS`", description="🔴 There are currently no `public` clans! Try again later, or create one.")
            await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if not ctx.author.bot:
            if config['Prefix'] in ctx.content:
                stats = levelling.find_one({"guildid": ctx.guild.id, "id": ctx.author.id})
                xp = stats["xp"]
                levelling.update_one({"guildid": ctx.guild.id, "name": f"{ctx.author}"}, {"$set": {"xp": xp}})
                return
            else:
                clan_search = levelling.find_one({"guildid": ctx.guild.id, "users": f"{ctx.author}"})
                if clan_search:
                    for x in clan_search['users']:
                        if x == str(ctx.author):
                            stats = levelling.find_one({"guildid": ctx.guild.id, "name": x})
                            serverstats = levelling.find_one({"server": ctx.guild.id})
                            levelling.update_one({"guildid": ctx.guild.id, "name": x}, {"$set": {"xp": stats['xp'] + serverstats['xp_per_message'] - serverstats['xp_per_message'], "total_xp": clan_search['total_xp'] + serverstats['xp_per_message']}})
                            levelling.update_one({"guildid": ctx.guild.id, "clan_name": clan_search['clan_name']}, {"$set": {"total_xp": clan_search['total_xp'] + serverstats['xp_per_message']}})

                        elif x != str(ctx.author):
                            stats = levelling.find_one({"guildid": ctx.guild.id, "name": x})
                            serverstats = levelling.find_one({"server": ctx.guild.id})
                            levelling.update_one({"guildid": ctx.guild.id, "name": x}, {"$set": {
                                "xp": stats['xp'] + serverstats['xp_per_message'] / 2}})



# Sets-up the cog for Profile+
def setup(client):
    client.add_cog(Clan(client))
