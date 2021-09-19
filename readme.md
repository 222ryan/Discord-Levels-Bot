# Getting Started
**First**, you will need an install of `Modern Levels` that supports this Documentation page (4.7.1 >). If you need assistance, please join the Discord Server.

## Importing
```from kumoslab.<get|getServer|set> import <function|*>```

# Getting User Information
- *This will retrieve specific information about users in a guild, such as their background url, current xp count, etc*

## backgroundUrl
```await backgroundURL(id=<user id>, guildID=<guild id>)```  
*Retrieves the users Background URL*

**Example:**  
1. ```background = backgroundUrl(id=ctx.author.id, guildID=ctx.guild.id)```   
2. ```await ctx.send(str(await background))```

## getXP
```await getXP(id=<user id>, guildID=<guild id>)```  
*Retrieves the users current XP amount*

**Example:**  
1. ```xp = getXP(id=ctx.author.id, guildID=ctx.guild.id)```   
2. ```await ctx.send(str(await xp))```

## getLevel
```await getLevel(id=<user id>, guildID=<guild id>)```  
*Retrieves the users current Level*

**Example:**  
1. ```level = getLevel(id=ctx.author.id, guildID=ctx.guild.id)```   
2. ```await ctx.send(str(await level))```

## getXPColour
```await getXPColour(id=<id>, guildID=<guild id>)```  
*Retrieves the users current xp colour*

**Example:**  
1. ```xp_colour = getXPColour(id=member.id, guildID=ctx.guild.id)```   
2. ```await ctx.send(str(await xp_colour))```

## getCirlce
```await getCirlce(id=<id>, guildID=<guild id>)```  
*Retrieves the users current state of their pfp (true/false)*

**Example:**  
1. ```circle = getCircle(id=member.id, guildID=ctx.guild.id)```   
2. ```await ctx.send(str(await circle))```

# Getting Server Information
- *This will retrive information about servers the bot is in*

## xpPerMessage
```await xpPerMessage(guildID=<guild id>)```  
*Retrieves the servers xp per message stat*

**Example:**  
1. ```xp_per_message = xpPerMessage(guildID=ctx.guild.id)```   
2. ```await ctx.send(str(await xp_per_message))```

## doubleXPRole
```await doubleXPRole(guildID=<guild id>)```  
*Retrieves the servers double xp role*

**Example:**  
1. ```doublexp_role = doubleXPRole(guildID=ctx.guild.id)```   
2. ```await ctx.send(str(await doublexp_role))```

## levelChannel
```await levelChannel(guildID=<guild id>)```  
*Retrieves the servers level channel*

**Example:**  
1. ```level_channel = levelChannel(guildID=ctx.guild.id)```   
2. ```await ctx.send(str(await level_channel))```

## getLevels
```await getLevels(guildID=<guild id>)```  
*Retrieves the servers levels for unlocking roles*

**Example:**  
1. ```levels = getLevels(guildID=ctx.guild.id)```   
2. ```await ctx.send(str(await levels))```

## getRoles
```await getRoles(guildID=<guild id>)```  
*Retrieves the servers roles for unlocking at a certain level*

**Example:**  
1. ```roles = getRoles(guildID=ctx.guild.id)```   
2. ```await ctx.send(str(await roles))```

## ignoredRole
```await ignoredRole(guildID=<guild id>)```  
*Retrieves the servers ignored role*

**Example:**  
1. ```ignored = ignoredRole(guildID=ctx.guild.id)```   
2. ```await ctx.send(str(await ignored))```

# Setting User Info
- *This will set a certain users stat*

## setXP
```await setXP(id=id, guildID=<guild id>, amount<int>)```  
*Sets the users xp*

**Example:**  
1. ```xp = setXP(id=id, guildID=ctx.guild.id, amount=10)```   
2. ```await ctx.send(str(await xp))```

## setBackground
```await setBackground(id=id, guildID=<guild id>, link=<link>)```  
*Sets the users background (if a link is invalid, it will set it to the deafult background)*

**Example:**  
1. ```background = setBackground(id=id, guildID=ctx.guild.id, link='https://www.google.com')```   
2. ```await ctx.send(str(await background))```

## setXPColour
```await setXPColour(id=id, guildID=<guild id>, hex=<hex code>)```  
*Sets the users xp colour*

**Example:**  
1. ```xp_colour = setXPColour(id=id, guildID=ctx.guild.id, hex_code='#ffffff')```   
2. ```await ctx.send(str(await xp_colour))```

## setCircle
```await setCircle(id=id, guildID=<guild id>, value=<True/False>)```  
*Sets the users circle pic state*

**Example:**  
1. ```circle = setCircle(id=id, guildID=ctx.guild.id, value=True)```   
2. ```await ctx.send(str(await circle))```
