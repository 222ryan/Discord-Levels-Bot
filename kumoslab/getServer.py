import discord
from Systems.levelsys import levelling


async def xpPerMessage(guildID=None):
    if guildID is None:
        print("xpPerMessage requires 'guildID'.")
        return
    else:
        try:
            stats = levelling.find_one({"server": guildID})
            xp_message = stats['xp_per_message']
            return str(xp_message)
        except Exception as e:
            print(f"xpPerMessage ran into an error!\n\n{e}")


async def doubleXPRole(guildID=None):
    if guildID is None:
        print("doubleXPRole requires 'guildID'.")
        return
    else:
        try:
            stats = levelling.find_one({"server": guildID})
            double_xp = stats['double_xp_role']
            return str(double_xp)
        except Exception as e:
            print(f"doubleXPRole ran into an error!\n\n{e}")


async def levelChannel(guildID=None):
    if guildID is None:
        print("levelChannel requires 'guildID'.")
        return
    else:
        try:
            stats = levelling.find_one({"server": guildID})
            level_channel = stats['level_channel']
            return str(level_channel)
        except Exception as e:
            print(f"levelChannel ran into an error!\n\n{e}")


async def getLevels(guildID=None):
    if guildID is None:
        print("getLevels requires 'guildID'.")
        return
    else:
        try:
            stats = levelling.find_one({"server": guildID})
            levels = stats['level']
            return str(levels)
        except Exception as e:
            print(f"getLevels ran into an error!\n\n{e}")


async def getRoles(guildID=None):
    if guildID is None:
        print("getRoles requires 'guildID'.")
        return
    else:
        try:
            stats = levelling.find_one({"server": guildID})
            roles = stats['role']
            return str(roles)
        except Exception as e:
            print(f"getRoles ran into an error!\n\n{e}")


async def ignoredRole(guildID=None):
    if guildID is None:
        print("ignoredRole requires 'guildID'.")
        return
    else:
        try:
            stats = levelling.find_one({"server": guildID})
            ignored_role = stats['ignoredRole']
            return str(ignored_role)
        except Exception as e:
            print(f"ignoredRole ran into an error!\n\n{e}")

