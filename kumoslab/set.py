import discord
from Systems.levelsys import levelling


async def setXP(id=None, guildID=None, amount=None):
    if id is None:
        print("setXP requires 'id'.")
        return
    if guildID is None:
        print("setXP requires 'guildID'.")
        return
    if amount is None:
        print("setXP requires 'amount'.")
        return
    else:
        try:
            stats = levelling.find_one({"guildid": guildID, "id": id})
            circle = stats['circle']
            levelling.update({"guildid": guildID, "id": id},
                             {"$set": {"xp": int(amount)}})
            return str(circle)
        except Exception as e:
            print(f"setXP ran into an error!\n\n{e}")


async def setBackground(id=None, guildID=None, link=None):
    if id is None:
        print("setXP requires 'id'.")
        return
    if guildID is None:
        print("setXP requires 'guildID'.")
        return
    if link is None:
        print("setBackground requires 'link'.")
        return
    else:
        try:
            levelling.update({"guildid": guildID, "id": id},
                             {"$set": {"background": str(link)}})
        except Exception as e:
            print(f"setBackground ran into an error!\n\n{e}")


async def setXPColour(id=None, guildID=None, hex_code=None):
    if id is None:
        print("setXP requires 'id'.")
        return
    if guildID is None:
        print("setXP requires 'guildID'.")
        return
    if hex_code is None:
        print("setBackground requires 'hex_code'.")
        return
    else:
        try:
            levelling.update({"guildid": guildID, "id": id},
                             {"$set": {"xp_colour": str(hex_code)}})
        except Exception as e:
            print(f"setXPColour ran into an error!\n\n{e}")


async def setCircle(id=None, guildID=None, value=None):
    if id is None:
        print("setCircle requires 'id'.")
        return
    if guildID is None:
        print("setCircle requires 'guildID'.")
        return
    if value is None:
        print("setCircle requires 'hex_code'.")
        return
    else:
        try:
            if value.lower() == "true":
                levelling.update_one({"guildid": guildID, "id": id}, {"$set": {"circle": True}})
            elif value.lower() == "false":
                levelling.update_one({"guildid": guildID, "id": id}, {"$set": {"circle": False}})
        except Exception as e:
            print(f"setCircle ran into an error!\n\n{e}")


