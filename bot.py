import discord
import random
import asyncio
import os
from pymongo import MongoClient
from datetime import datetime, timezone, timedelta
client = discord.Client()
cluster = MongoClient(str(os.environ.get('DB_CREDENTIALS')))
db = cluster["cases"]
adminarray = []
unixTime = round((datetime.now(timezone.utc) + timedelta(days=0)).timestamp())

# Support/Ticket System
# Automod (Mention spam, discord invites)
# Remind me
# Reaction Role
# Image Search and Google Search

def checkModRoles(message):
    if message.channel.permissions_for(message.author).administrator:
        return True
    else:
        roleList = []
        for role in message.author.roles:
            roleList.append(role.name)
        preferences = cluster["preferences"]
        serverID = preferences[str(message.channel.guild.id)]
        resultList = []
        results = serverID.find({})
        for result in results:
            resultList = result['admin-roles']
        a_set = set(resultList)
        b_set = set(roleList)
        if (a_set & b_set):
            return True
        else:
            return False


async def postCase(message, result):
    preferences = cluster["preferences"]
    preference = preferences[str(message.channel.guild.id)]
    j = ""
    results = preference.find({"mod-channel": {"$exists": False}})
    if results.count() == 0:
        results = preference.find({})
        for m in results:
            j = m
            modchannel = int(j['mod-channel'])
        modchannel = client.get_channel(modchannel)
        if result['case-type'].startswith("temp"):
            embed=discord.Embed(title="Case "+str(result['case-id']), description="ID: "+str(result['_id'])+"\nCase Type: "+str(result['case-type'])+"\nUser: <@"+str(result['user'])+">\nLength:  "+str(result['length'])+" seconds\nReason: "+str(result['reason'])+"\nModerator: "+str(result['moderator'])+"\n")
        else:
            embed=discord.Embed(title="Case "+str(result['case-id']), description="ID: "+str(result['_id'])+"\nCase Type: "+str(result['case-type'])+"\nUser: <@"+str(result['user'])+">\nReason: "+str(result['reason'])+"\nModerator: "+str(result['moderator'])+"\n")
        await modchannel.send(embed=embed)

async def automodPost(guild, post):
    preferences = cluster["preferences"]
    preference = preferences[str(guild.id)]
    j = ""
    results = preference.find({"mod-channel": {"$exists": False}})
    if results.count() == 0:
        results = preference.find({})
        for m in results:
            j = m
            modchannel = int(j['mod-channel'])
        modchannel = client.get_channel(modchannel)
        embed=discord.Embed(description=post, color=random.randint(0, 0xffffff))
        await modchannel.send(embed=embed)


@client.event
async def on_message(message):
    try:
        global adminarray
        global db
        global unixTime
        global collection
        tempPunishments = cluster["tempPunishments"]
        tempBans = tempPunishments["tempBans"]
        results = tempBans.find({})
        for i in results:
            if int(i['expiry']) < (datetime.now(timezone.utc) + timedelta(days=0)).timestamp():
                guild = client.get_guild(i['server-id'])
                user = client.get_user(int(i['user']))
                try:
                    await guild.unban(user)
                except:
                    pass
                tempBans.delete_one(i)
        tempMutes = tempPunishments["tempMutes"]
        results = tempMutes.find({})
        for i in results:
            if int(i['expiry']) < (datetime.now(timezone.utc) + timedelta(days=0)).timestamp():
                guild = client.get_guild(i['server-id'])
                user = guild.get_member(int(i['user']))
                role = discord.utils.get(guild.roles, name='Muted')
                await user.remove_roles(role)
                tempMutes.delete_one(i)
        if message.content == "h!lock":
            if checkModRoles(message=message) == True:
                bole = message.channel.guild.default_role
                overwrite = discord.PermissionOverwrite()
                overwrite.send_messages = False
                await message.channel.set_permissions(target=bole, overwrite=overwrite)
                await message.add_reaction("👍")
            else:
                await message.channel.send("You do not have the proper permissions to execute this command.")
        elif message.content.startswith("h!lock "):
            if checkModRoles(message=message) == True:
                param, warnList = message.content.split("h!lock ", 1)
                role = discord.utils.get(message.channel.guild.roles, name=warnList)
                if role == None:
                    raise Exception('Invalid role name.')
                else:
                    overwrite = discord.PermissionOverwrite()
                    overwrite.send_messages = False
                    await message.channel.set_permissions(target=role, overwrite=overwrite)
                    await message.add_reaction("👍")
            else:
                await message.channel.send("You do not have the proper permissions to execute this command.")
        if message.content == "h!unlock":
            if checkModRoles(message=message) == True:
                bole = message.channel.guild.default_role
                overwrite = discord.PermissionOverwrite()
                overwrite.send_messages = None
                await message.channel.set_permissions(target=bole, overwrite=overwrite)
                await message.add_reaction("👍")
            else:
                await message.channel.send("You do not have the proper permissions to execute this command.")
        elif message.content.startswith("h!unlock "):
            if checkModRoles(message=message) == True:
                param, warnList = message.content.split("h!unlock ", 1)
                role = discord.utils.get(message.channel.guild.roles, name=warnList)
                if role == None:
                    raise Exception('Invalid role name.')
                else:
                    overwrite = discord.PermissionOverwrite()
                    overwrite.send_messages = None
                    await message.channel.set_permissions(target=role, overwrite=overwrite)
                    await message.add_reaction("👍")
            else:
                await message.channel.send("You do not have the proper permissions to execute this command.")
        if message.content == "h!uptime":
            unixTime2 = round((datetime.now(timezone.utc) + timedelta(days=0)).timestamp())
            uptime = str(timedelta(seconds=unixTime2-unixTime))
            embed = discord.Embed(
                description="Uptime: **"+uptime+"**",
                color=random.randint(0, 0xffffff))
            await message.channel.send(embed=embed)
        if message.content == "h!case":
            await message.channel.send(
                "**Moderator Command** `Usage: h!case <number>`\n- Gives information about a specified case.")
        elif message.content.startswith("h!case"):
            if checkModRoles(message=message) == True:
                param, warnList = message.content.split("h!case ", 1)
                warnList = int(warnList)
                db = cluster["cases"]
                collection = db[str(message.channel.guild.id)]
                results = collection.find({'case-id': warnList})
                result = {}
                for i in results:
                    result = i
                if result == {}:
                    embed=discord.Embed(title="**Case Details**", description="This case does not exist!", color=random.randint(0, 0xffffff))
                    await message.channel.send(embed=embed)
                else:
                    if result['case-type'].startswith("temp"):
                        embed = discord.Embed(title="Details for Case " + str(result['case-id']),
                                              description="ID: " + str(result['_id']) + "\nCase Type: " + str(
                                                  result['case-type']) + "\nUser: <@" + str(
                                                  result['user']) + ">\nLength:  " + str(
                                                  result['length']) + " seconds\nReason: " + str(
                                                  result['reason']) + "\nModerator: " + str(result['moderator']) + "\n")
                    else:
                        embed = discord.Embed(title="Details for Case " + str(result['case-id']),
                                              description="ID: " + str(result['_id']) + "\nCase Type: " + str(
                                                  result['case-type']) + "\nUser: <@" + str(
                                                  result['user']) + ">\nReason: " + str(
                                                  result['reason']) + "\nModerator: " + str(result['moderator']) + "\n")
                    await message.channel.send(embed=embed)
        if message.content == "h!purge":
            await message.channel.send(
                "**Moderator Command** `Usage: h!purge <number>`\n- Purges a specified number of messages from chat. Event Horizon will not purge more than 1,000 messages per command. Messages must be younger than 14 days.")
        elif message.content.startswith("h!purge"):
            if checkModRoles(message=message) == True:
                param, warnList = message.content.split("h!purge ", 1)
                warnList = int(warnList)
                if warnList < 1001:
                    deleted = await message.channel.purge(limit=warnList+1)
                    await automodPost(message.channel.guild, "**Message purge executed in <#"+str(message.channel.id)+">**\nResponsible moderator: <@"+str(message.author.id)+">\nMessages deleted: "+str(len(deleted)-1))
                    await asyncio.sleep(2)
                else:
                    delmes = await message.channel.send("Event Horizon cannot purge more than 1,000 messages per command.")
                    await asyncio.sleep(2)
                    await delmes.delete()
        if message.content == "h!modchannel":
            if checkModRoles(message=message) == True:
                preferences = cluster["preferences"]
                tempBans = preferences[str(message.channel.guild.id)]
                z = ""
                results = tempBans.find({"mod-channel":{"$exists": False}})
                if results.count() == 1:
                    embed = discord.Embed(description="**You don't have a modlogs channel in this server. To set one up, use `h!modchannel <#channel>`.**",color=random.randint(0, 0xffffff))
                    await message.channel.send(embed=embed)
                else:
                    if str(message.channel.guild.id) in preferences.list_collection_names():
                        results = tempBans.find({})
                        for i in results:
                            z = i
                        modchannel = z['mod-channel']
                        embed = discord.Embed(
                            description="**Moderation actions are currently logged in <#"+str(modchannel)+">**. To change your mod channel, use `h!modchannel <#channel>`. To clear your mod channel, use `h!modchannel None`.",
                            color=random.randint(0, 0xffffff))
                        await message.channel.send(embed=embed)
                    else:
                        embed = discord.Embed(
                            description="**You don't have a modlogs channel in this server. To set one up, use `h!modchannel <#channel>`.**",
                            color=random.randint(0, 0xffffff))
                        await message.channel.send(embed=embed)
            else:
                await message.channel.send("You do not have the proper permissions to execute this command.")
        elif message.content.startswith("h!modchannel "):
            if checkModRoles(message=message) == True:
                param, logList = message.content.split("h!modchannel ", 1)
                preferences = cluster["preferences"]
                tempBans = preferences[str(message.channel.guild.id)]
                logList = (logList.split(" ", 1))
                logList = logList[0].replace("<", "")
                logList = logList.replace("!", "")
                logList = logList.replace("#", "")
                logList = logList.replace(">", "")
                if logList == "None":
                    tempBans.update_one({}, {"$unset":{"mod-channel":1}})
                    embed = discord.Embed(
                        description="**Moderation actions will no longer be logged.** To change your mod channel, use `h!modchannel <#channel>`. To clear your mod channel, use `h!modchannel None`.",
                        color=random.randint(0, 0xffffff))
                    await message.channel.send(embed=embed)
                else:
                    logList = int(logList)
                    channelList = []
                    for i in message.channel.guild.channels:
                        channelList.append(i.id)
                    if int(logList) in channelList:
                        preferences = cluster["preferences"]
                        if str(message.channel.guild.id) in preferences.list_collection_names():
                            tempBans = preferences[str(message.channel.guild.id)]
                            tempBans.update_one({}, {"$set": {"mod-channel": str(logList)}})
                        else:
                            id = round((datetime.now(timezone.utc) + timedelta(
                                days=0)).timestamp() * 1000000 - 1593028107000000)
                            tempBans = preferences[str(message.channel.guild.id)]
                            tempBans.insert_one({"_id": id, "admin-roles": [], "mod-channel": str(logList)})
                        embed = discord.Embed(
                            description="**Moderation actions will now be logged in <#" + str(
                                logList) + ">**. To change your mod channel, use `h!modchannel <#channel>`. To clear your mod channel, use `h!modchannel None`.",
                            color=random.randint(0, 0xffffff))
                        await message.channel.send(embed=embed)
                    else:
                        raise Exception("That channel is not in your server!")
            else:
                await message.channel.send("You do not have the proper permissions to execute this command.")
        if message.content == "h!donate":
            await message.channel.send("Help support the development and running of Event Horizon. Patreon: https://www.patreon.com/eddyzow")
        if message.content == "h!help":
            await message.add_reaction("👍")
            embed = discord.Embed(title="**Commands**", description="To view a full list of commands, visit Event Horizon's website.\nhttps://eddyzhao828.wixsite.com/event-horizon/",color=random.randint(0, 0xffffff))
            await message.author.send(embed=embed)
        if message.content == "h!changelog":
            embed=discord.Embed(title="**Changelog**", description="v1.0.2 Changelog (6/28/2020)\n\n**New commands added in this release:**\nh!vcrole, h!vcroles.")
            await message.channel.send(embed=embed)
        if message.content == "h!membercount":
            guild = message.channel.guild
            await message.channel.send("**"+str(guild.name)+"** currently has **"+str(guild.member_count)+"** members.")
        if message.content == "h!info":
            await message.author.send("**To invite Event Horizon to your Discord server, use this link!**\nhttps://discord.com/oauth2/authorize?client_id=725212443361673256&scope=bot&permissions=8")
        if message.content == "h!modroles":
            if checkModRoles(message=message) == True:
                preferences = cluster["preferences"]
                tempBans = preferences[str(message.channel.guild.id)]
                results = tempBans.find({})
                resultlength = 0
                for i in results:
                    adminroles = i['admin-roles']
                    resultlength += 1
                if resultlength == 0:
                    embed = discord.Embed(description="You have not added any modroles to this server. **Any user with the Administrator property may use moderator commands.**\n\nTo add modroles, use this syntax: `Usage: h!modroles <role name to add/remove>`\nModroles are case-sensitive and will fail if you do not type the role as it is listed.",
                                          color=random.randint(0, 0xffffff))
                    await message.channel.send(embed=embed)
                else:
                    output = "**"
                    for i in adminroles:
                        output = output + i + "\n"
                    if len(adminroles) == 0:
                        output = "Currently, there are no specific modroles assigned to this server.**\n"
                    embed = discord.Embed(
                        description="Modroles:\n"+output+"**\n**Any user with the Administrator property may use moderator commands.**\n\nTo add modroles, use this syntax: `Usage: h!modroles <role name to add/remove>`\nModroles are case-sensitive and will fail if you do not type the role as it is listed.",
                        color=random.randint(0, 0xffffff))
                    await message.channel.send(embed=embed)
            else:
                await message.channel.send("You do not have the proper permissions to execute this command.")
        elif message.content.startswith("h!modroles"):
            if checkModRoles(message=message) == True:
                param, warnList = message.content.split("h!modroles ", 1)
                roleList = []
                for rolee in message.channel.guild.roles:
                    roleList.append(rolee.name)
                if warnList in roleList:
                    preferences = cluster["preferences"]
                    tempBans = preferences[str(message.channel.guild.id)]
                    results = tempBans.find({})
                    for i in results:
                        adminarray = i['admin-roles']
                    remove=0
                    if warnList in adminarray and len(adminarray) != 0:
                        remove=1
                        adminarray.remove(warnList)
                    else:
                        adminarray.append(warnList)
                    if tempBans.count() == 0:
                        id = round(
                            (datetime.now(timezone.utc) + timedelta(days=0)).timestamp() * 1000000 - 1593028107000000)
                        result = {"_id": id, "admin-roles": []}
                        tempBans.insert_one(result)
                    tempBans.update_one({},{"$set":{"admin-roles": adminarray}})
                    if remove==0:
                        embed = discord.Embed(
                            description="**\✅ Added role +"+str(warnList)+" to modroles for this server.**\nYou can view existing modroles with `h!modroles`.",
                            color=random.randint(0, 0xffffff))
                    else:
                        embed = discord.Embed(
                            description="**\✅ Removed role -" + str(warnList) + " from modroles for this server.**\nYou can view existing modroles with `h!modroles`.",
                            color=random.randint(0, 0xffffff))
                    await message.channel.send(embed=embed)
                else:
                    embed = discord.Embed(
                        description="**\❌ Role " + str(
                            warnList) + " does not exist.**",
                        color=random.randint(0, 0xffffff))
                    await message.channel.send(embed=embed)
            else:
                await message.channel.send("You do not have the proper permissions to execute this command.")
        if message.content == "h!warn":
            await message.channel.send("**Moderator Command** `Usage: h!warn <@user> <reason>`\n- Warns specified user.")
        elif message.content == "h!warnings":
            db = cluster["cases"]
            collection = db[str(message.channel.guild.id)]
            results = collection.find({'case-type': "warn", 'user': str(message.author.id)})
            finalList = []
            for i in results:
                finalList.append(i)
            desc = ""
            for i in finalList:
                desc = desc + "**ID: **"+str(i['_id'])+"\n**Case ID:** "+str(i['case-id'])+"\n**User:** <@"+str(i['user'])+">\n**Moderator:** "+str(i['moderator'])+"\n**Reason:** "+str(i['reason']+"\n\n")
            if desc == "":
                desc = "No warnings to display."
            embed=discord.Embed(title="**Warnings for "+str(message.author)+"**", description=desc)
            await message.channel.send(embed=embed)
        elif message.content.startswith("h!warn"):
            if checkModRoles(message=message) == True:
                param, warnList = message.content.split("h!warn ", 1)
                warnList = (warnList.split(" ", 1))
                reason = warnList[1]
                user = warnList[0]
                user = user.replace("<", "")
                user = user.replace("@", "")
                user = user.replace("!", "")
                user = user.replace(">", "")
                pingUser = client.get_user(int(user))
                db = cluster["cases"]
                collection = db[str(message.channel.guild.id)]
                numberOfCases = collection.count()
                id = round((datetime.now(timezone.utc) + timedelta(days=0)).timestamp() * 1000000 - 1593028107000000)
                result = {"_id": id, "case-id": numberOfCases+1, "case-type": "warn", "user": str(user),
                          "reason": reason, "moderator": str(message.author)}
                collection.insert_one(result)
                try:
                    await postCase(message, result)
                except:
                    pass
                try:
                    embed=discord.Embed(title="**Punishment**", description="**You have been warned in "+str(message.channel.guild)+". Reason: "+str(warnList[1])+".**", color=0xff0000)
                    await pingUser.send(embed=embed)
                    embed=discord.Embed(title="\✅ ***Case "+str(numberOfCases+1)+": "+str(pingUser)+" has been warned. Reason: "+str(warnList[1])+"***", color=random.randint(0, 0xffffff))
                    await message.channel.send(embed=embed)
                except:
                    embed = discord.Embed(title="\✅ ***Case " + str(numberOfCases + 1) + ": Warning logged for " + str(
                        pingUser) + ". They were not warned. Reason: " + str(warnList[1]) + "***", color=random.randint(0, 0xffffff))
                    try:
                        await message.channel.send(embed=embed)
                    except:
                        pass
            else:
                await message.channel.send("You do not have the proper permissions to execute this command.")
        if message.content == "h!joinage":
            if checkModRoles(message=message) == True:
                preferences = cluster["preferences"]
                if str(message.channel.guild.id) not in preferences.list_collection_names():
                    id = round((datetime.now(timezone.utc) + timedelta(
                        days=0)).timestamp() * 1000000 - 1593028107000000)
                    tempBans = preferences[str(message.channel.guild.id)]
                    tempBans.insert_one({"_id": id, "admin-roles": []})
                tempBans = preferences[str(message.channel.guild.id)]
                results = tempBans.find({})
                result = {}
                for i in results:
                    result = i
                if 'join-age' in result:
                    if result['join-age'] == 0:
                        embed = discord.Embed(title="Server Join Age", description=str(message.channel.guild.name)+" does not currently have a minimum join age. To set one, use `h!setjoinage`.", color=random.randint(0, 0xffffff))
                        await message.channel.send(embed=embed)

                    else:
                        embed = discord.Embed(title="Server Join Age", description=str(message.channel.guild.name)+"'s minimum join age is currently set to **"+str(result['join-age'])+" days**.", color=random.randint(0, 0xffffff))
                        await message.channel.send(embed=embed)
                else:
                    embed = discord.Embed(title="Server Join Age", description=str(
                        message.channel.guild.name) + " does not currently have a minimum join age. To set one, use `h!setjoinage`.",
                                          color=random.randint(0, 0xffffff))
                    await message.channel.send(embed=embed)


            else:
                await message.channel.send("You do not have the proper permissions to execute this command.")
        if message.content == "h!vcroles":
            if checkModRoles(message=message) == True:
                preferences = cluster["preferences"]
                if str(message.channel.guild.id) not in preferences.list_collection_names():
                    id = round((datetime.now(timezone.utc) + timedelta(
                        days=0)).timestamp() * 1000000 - 1593028107000000)
                    tempBans = preferences[str(message.channel.guild.id)]
                    tempBans.insert_one({"_id": id, "admin-roles": [], 'vc-roles': {}})
                tempBans = preferences[str(message.channel.guild.id)]
                results = tempBans.find({})
                for i in results:
                    result = i
                if 'vc-roles' in result:
                    vcRoles = result['vc-roles']
                else:
                    vcRoles = {}
                roles = {}
                for i in vcRoles:
                    if len(vcRoles[i]) > 0:
                        roles[i] = vcRoles[i]
                print(roles)
                roless = []
                channels = []
                for i in roles:
                    channels.append(client.get_channel(int(i)).id)
                for i in roles:
                    roless.append(roles[i])
                print(channels)
                print(roless)
                channelValue = ""
                roleValue = ""
                for i in channels:
                    channelf = client.get_channel(int(i))
                    channelValue = channelValue + str(channelf.name) + "\n"
                for i in roless:
                    lenner = 0
                    for g in i:
                        lenner += 1
                        role = discord.utils.get(message.channel.guild.roles, id=int(g))
                        if lenner == len(i):
                            roleValue = roleValue + str(role.name)
                        else:
                            roleValue = roleValue + str(role.name) + ", "
                    roleValue = roleValue + "\n"
                if channelValue == "" and roleValue == "":
                    embed = discord.Embed(title="**VC Roles**",
                                          description="You have no VC roles.\n\nTo add a VC role, join the specified voice channel and use `h!vcrole <role name>`.",
                                          color=random.randint(0, 0xffffff))
                    await message.channel.send(embed=embed)
                    return
                embed = discord.Embed(title="**VC Roles**", description="To remove a VC role, join the specified voice channel and use `h!vcrole <role name>`.", color=random.randint(0,0xffffff))
                embed.add_field(name="Channels", value=channelValue, inline=True)
                embed.add_field(name="Roles", value=roleValue, inline=True)
                await message.channel.send(embed=embed)




            else:
                await message.channel.send("You do not have the proper permissions to execute this command.")
        if message.content == "h!vcrole":
            await message.channel.send("**Moderator Command** `Usage: h!vcrole <role name to add or remove>`\n- Gives the specified role to anyone who joins the voice channel moderator is in. Also takes the role when user leaves. To remove an already existing VC role, just run the command as is. To get a list of VC roles, use `h!vcroles`.")
        elif message.content.startswith("h!vcrole "):
            if checkModRoles(message=message) == True:
                param, warnList = message.content.split("h!vcrole ", 1)
                if message.author.voice == None:
                    raise Exception("You must be in a voice channel.")
                else:
                    vc = message.author.voice.channel.id
                    channels = []
                    for channelz in message.guild.channels:
                        channels.append(channelz.id)
                    if vc not in channels:
                        raise Exception("You cannot control a VC role for a VC that is not in your server.")
                    role = discord.utils.get(message.channel.guild.roles, name=str(warnList))
                    if role == None:
                        raise Exception("That role does not exist in this server. Input must be case-sensitive.")
                    else:
                        preferences = cluster["preferences"]
                        if str(message.channel.guild.id) not in preferences.list_collection_names():
                            id = round((datetime.now(timezone.utc) + timedelta(
                                days=0)).timestamp() * 1000000 - 1593028107000000)
                            tempBans = preferences[str(message.channel.guild.id)]
                            tempBans.insert_one({"_id": id, "admin-roles": [], 'vc-roles': {}})
                        tempBans = preferences[str(message.channel.guild.id)]
                        results = tempBans.find({})
                        for i in results:
                            result = i
                        if 'vc-roles' in result:
                            vcRoles = result['vc-roles']
                        else:
                            vcRoles = {}
                        if str(vc) not in vcRoles:
                            vcRoles[str(vc)] = []
                        if str(role.id) in vcRoles[str(vc)]:
                            vcRoles[str(vc)].remove(str(role.id))
                            embed = discord.Embed(title="**VC Role**", description="Users who join **" + str(
                                message.author.voice.channel.name) + "** voice channel will no longer get the **" + str(
                                role.name) + "** role.", color=random.randint(0, 0xffffff))
                            try:
                                await message.author.remove_roles(role)
                            except:
                                pass

                        else:
                            vcRoles[str(vc)].append(str(role.id))
                            embed = discord.Embed(title="**VC Role**", description="Users who join **" + str(
                                message.author.voice.channel.name) + "** voice channel will now get the **" + str(
                                role.name) + "** role.", color=random.randint(0, 0xffffff))

                        tempBans.update_one({}, {"$set": {"vc-roles":vcRoles}})
                        await message.channel.send(embed=embed)

            else:
                await message.channel.send("You do not have the proper permissions to execute this command.")
        if message.content == "h!setjoinage":
            await message.channel.send("**Moderator Command** `Usage: h!setjoinage <number of days>`\n- Sets the minimum account age to enter the server. Useful for defending against alt accounts. To turn minimum join age off, set the join age to 0. To view your server's join age, use `h!joinage`.")
        elif message.content.startswith("h!setjoinage "):
            if checkModRoles(message=message) == True:
                param, warnList = message.content.split("h!setjoinage ", 1)
                warnList = int(warnList)
                if warnList < 0:
                    raise Exception("You can't set joinage to under 0 days.")
                if warnList > 365:
                    raise Exception("You can't set joinage to over 365 days.")
                preferences = cluster["preferences"]
                serverID = preferences[str(message.channel.guild.id)]
                if str(message.channel.guild.id) in preferences.list_collection_names():
                    tempBans = preferences[str(message.channel.guild.id)]
                    tempBans.update_one({}, {"$set": {"join-age": warnList}})
                else:
                    id = round((datetime.now(timezone.utc) + timedelta(
                        days=0)).timestamp() * 1000000 - 1593028107000000)
                    tempBans = preferences[str(message.channel.guild.id)]
                    tempBans.insert_one({"_id": id, "admin-roles": [], "join-age": warnList})
                if warnList == 0:
                    embed = discord.Embed(title="**Set Joinage**", description=str(message.channel.guild.name)+"'s minimum join age has been turned off.", color=random.randint(0, 0xffffff))

                else:
                    embed = discord.Embed(title="**Set Joinage**", description=str(message.channel.guild.name)+"'s minimum join age has been set to **"+str(warnList)+" days**.", color=random.randint(0, 0xffffff))
                await message.channel.send(embed=embed)
            else:
                await message.channel.send("You do not have the proper permissions to execute this command.")
        if message.content == "h!poll":
            await message.channel.send("`Usage: h!poll <poll>`\n- Sends a poll.")
        elif message.content.startswith("h!poll "):
            param, warnList = message.content.split("h!poll ", 1)
            embed=discord.Embed(title="**Poll**", description=warnList, color=random.randint(0, 0xffffff))
            fmes = await message.channel.send(embed=embed)
            await fmes.add_reaction("👍")
            await fmes.add_reaction("👎")
            await fmes.add_reaction('🤷')
        if message.content == "h!ban":
            await message.channel.send("**Moderator Command** `Usage: h!ban <@user> <reason>`\n- Bans specified user from the server command is executed in. To temp-ban someone, see `h!tempban`.")
        elif message.content.startswith("h!ban"):
            if checkModRoles(message=message) == True:
                param, warnList = message.content.split("h!ban ", 1)
                warnList = (warnList.split(" ", 1))
                try:
                    reason = warnList[1]
                except:
                    reason = "No reason specified"
                user = warnList[0]
                user = user.replace("<", "")
                user = user.replace("@", "")
                user = user.replace("!", "")
                user = user.replace(">", "")
                pingUser = client.get_user(int(user))
                db = cluster["cases"]
                collection = db[str(message.channel.guild.id)]
                numberOfCases = collection.count()
                id = round((datetime.now(timezone.utc) + timedelta(days=0)).timestamp() * 1000000 - 1593028107000000)
                result = {"_id": id, "case-id": numberOfCases+1, "case-type": "ban", "user": str(user),
                          "reason": reason, "moderator": str(message.author)}
                collection.insert_one(result)
                try:
                    await postCase(message, result)
                except:
                    pass
                try:
                    embed = discord.Embed(title="**Punishment**", description="*You have been banned from "+str(message.channel.guild)+". Reason: "+reason+".**", color=0xff0000)
                    await pingUser.send(embed=embed)
                    await message.channel.guild.ban(pingUser, delete_message_days=7)
                    embed=discord.Embed(title="\✅ ***Case "+str(numberOfCases+1)+": "+str(pingUser)+" has been banned. Reason: "+reason+"***", color=random.randint(0, 0xffffff))
                    await message.channel.send(embed=embed)
                except:
                    await message.channel.guild.ban(pingUser, delete_message_days=7)
                    embed = discord.Embed(title="\✅ ***Case " + str(numberOfCases + 1) + ": " + str(
                        pingUser) + " has been banned. Reason: " + reason + "***",
                                          color=random.randint(0, 0xffffff))
                    await message.channel.send(embed=embed)
            else:
                await message.channel.send("You do not have the proper permissions to execute this command.")
        if message.content == "h!kick":
            await message.channel.send("**Moderator Command** `Usage: h!kick <@user> <reason>`\n- Kicks specified user from the server command is executed in.")
        elif message.content.startswith("h!kick"):
            if checkModRoles(message=message) == True:
                param, warnList = message.content.split("h!kick ", 1)
                warnList = (warnList.split(" ", 1))
                try:
                    reason = warnList[1]
                except:
                    reason = "No reason specified"
                user = warnList[0]
                user = user.replace("<", "")
                user = user.replace("@", "")
                user = user.replace("!", "")
                user = user.replace(">", "")
                pingUser = client.get_user(int(user))
                db = cluster["cases"]
                collection = db[str(message.channel.guild.id)]
                numberOfCases = collection.count()
                id = round((datetime.now(timezone.utc) + timedelta(days=0)).timestamp() * 1000000 - 1593028107000000)
                result = {"_id": id, "case-id": numberOfCases+1, "case-type": "kick", "user": str(user),
                          "reason": reason, "moderator": str(message.author)}
                collection.insert_one(result)
                try:
                    await postCase(message, result)
                except:
                    pass
                try:
                    embed = discord.Embed(title="**Punishment**", description="*You have been kicked from "+str(message.channel.guild)+". Reason: "+reason+".**", color=0xff0000)
                    await pingUser.send(embed=embed)
                    await message.channel.guild.kick(pingUser)
                    embed=discord.Embed(title="\✅ ***Case "+str(numberOfCases+1)+": "+str(pingUser)+" has been kicked. Reason: "+reason+"***", color=random.randint(0, 0xffffff))
                    await message.channel.send(embed=embed)
                except:
                    await message.channel.guild.kick(pingUser)
                    embed = discord.Embed(title="\✅ ***Case " + str(numberOfCases + 1) + ": " + str(
                        pingUser) + " has been kicked. Reason: " + reason + "***",
                                          color=random.randint(0, 0xffffff))
                    await message.channel.send(embed=embed)
            else:
                await message.channel.send("You do not have the proper permissions to execute this command.")
        if message.content == "h!unmute":
            await message.channel.send("**Moderator Command** `Usage: h!unmute <@user>`\n- Unmutes specified user from the server command is executed in.")
        elif message.content.startswith("h!unmute "):
            if checkModRoles(message=message) == True:
                param, logList = message.content.split("h!unmute ", 1)
                logList = (logList.split(" ", 1))
                logList = logList[0].replace("<", "")
                logList = logList.replace("!", "")
                logList = logList.replace("@", "")
                logList = logList.replace(">", "")
                pingUser = client.get_user(int(logList))
                pingMember = message.channel.guild.get_member(int(logList))
                try:
                    role = discord.utils.get(message.channel.guild.roles, name='Muted')
                    if role in pingMember.roles:
                        await pingMember.remove_roles(role)
                        embed = discord.Embed(title="\✅ **" + str(
                            pingUser) + " has been unmuted.**", color=random.randint(0, 0xffffff))
                        await message.channel.send(embed=embed)
                    else:
                        embed = discord.Embed(title="\❌ **" + str(
                            pingUser) + " couldn't be unmuted.**", description="Maybe they are not muted after all!",
                                              color=random.randint(0, 0xffffff))
                        await message.channel.send(embed=embed)
                except:
                    embed = discord.Embed(title="\❌ **" + str(
                        pingUser) + " couldn't be unmuted.**", description="Maybe they are not muted after all!", color=random.randint(0, 0xffffff))
                    await message.channel.send(embed=embed)
            else:
                await message.channel.send("You do not have the proper permissions to execute this command.")
        if message.content == "h!unban":
            await message.channel.send(
                "**Moderator Command** `Usage: h!unban <@user>`\n- Unbans specified user from the server command is executed in.")
        elif message.content.startswith("h!unban "):
            if checkModRoles(message=message) == True:
                param, logList = message.content.split("h!unban ", 1)
                logList = (logList.split(" ", 1))
                logList = logList[0].replace("<", "")
                logList = logList.replace("!", "")
                logList = logList.replace("@", "")
                logList = logList.replace(">", "")
                pingUser = client.get_user(int(logList))
                try:
                    await message.channel.guild.unban(pingUser)
                    embed = discord.Embed(title="\✅ **" + str(
                        pingUser) + " has been unbanned.**", color=random.randint(0, 0xffffff))
                    await message.channel.send(embed=embed)
                except:
                    embed = discord.Embed(title="\❌ **" + str(
                        pingUser) + " couldn't be unbanned.**", description="Maybe they are not banned after all!", color=random.randint(0, 0xffffff))
                    await message.channel.send(embed=embed)
            else:
                await message.channel.send("You do not have the proper permissions to execute this command.")

        if message.content == "h!topic":
            await message.channel.send("**Moderator Command** `Usage: h!topic <topic>`\n- Changes the topic of the channel command is executed in.")

        elif message.content.startswith("h!topic "):
            if checkModRoles(message=message) == True:
                param, term = message.content.split("!topic ", 1)
                await message.channel.edit(topic=str(term))
                await message.add_reaction("✅")
            else:
                await message.channel.send("You do not have the proper permissions to execute this command.")

        if message.content == "h!modlogs":
            await message.channel.send("**Moderator Command** `Usage: h!modlogs <@user>`\n- Returns all server mod logs for specified user.")

        elif message.content.startswith("h!modlogs "):
            if checkModRoles(message=message) == True:
                param, logList = message.content.split("h!modlogs ", 1)
                logList = (logList.split(" ", 1))
                logList = logList[0].replace("<", "")
                logList = logList.replace("!", "")
                logList = logList.replace("@", "")
                logList = logList.replace(">", "")
                db = cluster["cases"]
                collection = db[str(message.channel.guild.id)]
                results = collection.find({"user": str(logList)})
                lenz = 0
                for result in results:
                    if str(result['case-type']) == "tempban" and str(result['case-type']) == "tempmute":
                        embed = discord.Embed(title="**Case " + str(result['case-id']) + "**",
                                              description="ID: " + str(result['_id']) + "\nCase Type: " + str(
                                                  result['case-type']) + "\nUser: <@" + str(
                                                  result['user']) + ">\nLength: " + str(result['length']) + "\nReason: " + str(result['reason'])+"\nResponsible Moderator: "+str(result['moderator']), color=0x00ff00)
                        await message.channel.send(embed=embed)
                        lenz += 1
                    else:
                        embed=discord.Embed(title="**Case "+str(result['case-id'])+"**", description="ID: "+str(result['_id'])+"\nCase Type: "+str(result['case-type'])+"\nUser: <@"+str(result['user'])+">\nReason: "+str(result['reason'])+"\nResponsible Moderator: "+str(result['moderator']), color=0x00ff00)
                        await message.channel.send(embed=embed)
                        lenz += 1
                if lenz == 0:
                    embed = discord.Embed(title="**Modlogs**", description="No modlogs for this user!", color=0x00ff00)
                    await message.channel.send(embed=embed)
            else:
                await message.channel.send("You do not have the proper permissions to execute this command.")

        if message.content == "h!tempban":
            await message.channel.send("**Moderator Command** `Usage: h!tempban <@user> <time> <reason>`\n- Temporarily bans specified user from the server command is executed in. For time, use a number followed by suffix s, m, h, or d, meaning second, minute, hour, and day. Tempbans are limited to 30 days.")
        elif message.content.startswith("h!tempban"):
            if checkModRoles(message=message) == True:
                param, warnList = message.content.split("h!tempban ", 3)
                warnList = (warnList.split(" ", 2))
                time = warnList[1]
                if str(time).endswith("d"):
                    time = int(time.split("d")[0]) * 86400
                if str(time).endswith("h"):
                    time = int(time.split("h")[0]) * 3600
                if str(time).endswith("m"):
                    time = int(time.split("m")[0]) * 60
                if str(time).endswith("s"):
                    time = int(time.split("s")[0]) * 1
                if time > 2592000:
                    raise Exception("Tempbans are limited to 30 days.")
                try:
                    reason = warnList[2]
                except:
                    reason = "No reason specified"
                expiry = int((datetime.now(timezone.utc) + timedelta(days=0)).timestamp())+time
                user = warnList[0]
                user = user.replace("<", "")
                user = user.replace("@", "")
                user = user.replace("!", "")
                user = user.replace(">", "")
                pingUser = client.get_user(int(user))

                db = cluster["cases"]
                collection = db[str(message.channel.guild.id)]
                numberOfCases = collection.count()
                id = round((datetime.now(timezone.utc) + timedelta(days=0)).timestamp() * 1000000 - 1593028107000000)
                resultz = {"_id": id, "case-id": numberOfCases+1, "case-type": "tempban", "user": str(user), "length": int(time),
                          "reason": reason, "expiry": expiry, "moderator": str(message.author)}
                collection.insert_one(resultz)
                db = cluster["tempPunishments"]
                collection = db["tempBans"]
                resultz = {"_id": id, "server-id": message.channel.guild.id, "case-type": "tempban", "user": str(user),
                          "length": int(time),
                          "reason": reason, "expiry": expiry, "moderator": str(message.author)}
                collection.insert_one(resultz)
                try:
                    await postCase(message, result)
                except:
                    pass
                try:
                    embed = discord.Embed(title="**Punishment**", description="**You have been temporarily banned from "+str(message.channel.guild)+". Length: "+str(time)+" seconds. Reason: "+reason+".**", color=0xff0000)
                    await pingUser.send(embed=embed)
                    await message.channel.guild.ban(pingUser, delete_message_days=7)
                    embed=discord.Embed(title="\✅ ***Case "+str(numberOfCases+1)+": "+str(pingUser)+" has been tempbanned. Length: "+str(time)+" seconds. Reason: "+reason+"***", color=random.randint(0, 0xffffff))
                    await message.channel.send(embed=embed)
                except:
                    await message.channel.guild.ban(pingUser, delete_message_days=7)
                    embed = discord.Embed(title="\✅ ***Case " + str(numberOfCases + 1) + ": " + str(
                        pingUser) + " has been tempbanned. Length: "+str(time)+" seconds. Reason: " + reason + "***",
                                          color=random.randint(0, 0xffffff))
                    await message.channel.send(embed=embed)
            else:
                await message.channel.send("You do not have the proper permissions to execute this command.")



        if message.content == "h!tempmute":
            await message.channel.send("**Moderator Command** `Usage: h!tempmute <@user> <time> <reason>`\n- Temporarily mutes specified user from chatting in the server command is executed in. For time, use a number followed by suffix s, m, h, or d, meaning second, minute, hour, and day. Tempmutes are limited to 30 days. If a Muted role does not exist in the server, Event Horizon will create one.")
        elif message.content.startswith("h!tempmute"):
            if checkModRoles(message=message) == True:
                param, warnList = message.content.split("h!tempmute ", 3)
                warnList = (warnList.split(" ", 2))
                time = warnList[1]
                if str(time).endswith("d"):
                    time = int(time.split("d")[0]) * 86400
                if str(time).endswith("h"):
                    time = int(time.split("h")[0]) * 3600
                if str(time).endswith("m"):
                    time = int(time.split("m")[0]) * 60
                if str(time).endswith("s"):
                    time = int(time.split("s")[0]) * 1
                if time > 2592000:
                    raise Exception("Tempmutes are limited to 30 days.")
                try:
                    reason = warnList[2]
                except:
                    reason = "No reason specified"
                expiry = int((datetime.now(timezone.utc) + timedelta(days=0)).timestamp())+time
                user = warnList[0]
                user = user.replace("<", "")
                user = user.replace("@", "")
                user = user.replace("!", "")
                user = user.replace(">", "")
                pingUser = client.get_user(int(user))
                pingMember = message.guild.get_member(int(user))
                role = discord.utils.get(message.channel.guild.roles, name='Muted')
                if role not in pingMember.roles:
                    db = cluster["cases"]
                    collectione = db[str(message.channel.guild.id)]
                    numberOfCases = collectione.count()
                    id = round((datetime.now(timezone.utc) + timedelta(days=0)).timestamp() * 1000000 - 1593028107000000)
                    resultf = {"_id": id, "case-id": numberOfCases+1, "case-type": "tempmute", "user": str(user), "length": int(time),
                              "reason": reason, "expiry": expiry, "moderator": str(message.author)}
                    collectione.insert_one(resultf)
                    try:
                        await postCase(message, result)
                    except:
                        pass
                    db = cluster["tempPunishments"]
                    collectionz = db["tempMutes"]
                    resultf = {"_id": id, "server-id": message.channel.guild.id, "case-type": "tempmute", "user": str(user),
                              "length": int(time),
                              "reason": reason, "expiry": expiry, "moderator": str(message.author)}
                    collectionz.insert_one(resultf)
                    try:
                        await postCase(message, result)
                    except:
                        pass
                    try:
                        mutedrole = 0
                        for i in message.channel.guild.roles:
                            if i.name == "Muted":
                                mutedrole=i
                        if mutedrole == 0:
                            perms = discord.Permissions()
                            perms.update(send_messages=False, speak=False, send_tts_messages=False)
                            mutedrole = await message.channel.guild.create_role(name="Muted", permissions=perms, color=discord.Colour(0x1b1b1b))
                            await message.channel.send("Event Horizon did not detect a muted role in your server, so it created one for you.")
                        for channel in message.channel.guild.channels:
                            await channel.set_permissions(mutedrole, send_messages=False, speak=False, send_tts_messages=False)
                        await pingMember.add_roles(mutedrole)
                        embed = discord.Embed(title="**Punishment**",
                                              description="**You have been temporarily muted from " + str(
                            message.channel.guild) + ". Length: " + str(time) + " seconds. Reason: " + reason + ".**", color=0xff0000)
                        await pingUser.send(embed=embed)
                        embed=discord.Embed(title="\✅ ***Case "+str(numberOfCases+1)+": "+str(pingUser)+" has been tempmuted. Length: "+str(time)+" seconds. Reason: "+reason+"***", color=random.randint(0, 0xffffff))
                        await message.channel.send(embed=embed)
                    except:
                        mutedrole = 0
                        for i in message.channel.guild.roles:
                            if i.name == "Muted":
                                mutedrole = i
                        if mutedrole == 0:
                            perms = discord.Permissions()
                            perms.update(send_messages=False, speak=False, send_tts_messages=False)
                            mutedrole = await message.channel.guild.create_role(name="Muted", permissions=perms, color=discord.Colour(0x1b1b1b))
                            await message.channel.send(
                                    "Event Horizon did not detect a muted role in your server, so it created one for you.")
                        for channel in message.channel.guild.channels:
                            await channel.set_permissions(mutedrole, send_messages=False, speak=False, send_tts_messages=False)
                        await pingMember.add_roles(mutedrole)
                        embed = discord.Embed(title="\✅ ***Case " + str(numberOfCases + 1) + ": " + str(
                            pingUser) + " has been tempmuted. Length: "+str(time)+" seconds. Reason: " + reason + "***",
                                              color=random.randint(0, 0xffffff))
                        await message.channel.send(embed=embed)
                else:
                    embed = discord.Embed(description="Can't mute. User is already muted.",
                                          color=random.randint(0, 0xffffff))
                    await message.channel.send(embed=embed)
            else:
                await message.channel.send("You do not have the proper permissions to execute this command.")

        if message.content == "h!mute":
            await message.channel.send("**Moderator Command** `Usage: h!mute <@user> <reason>`\n- Mutes specified user from the server command is executed in. To temp-mute someone, see `h!tempmute`.")
        elif message.content.startswith("h!mute"):
            if checkModRoles(message=message) == True:
                param, warnList = message.content.split("h!mute ", 1)
                warnList = (warnList.split(" ", 1))
                try:
                    reason = warnList[1]
                except:
                    reason = "No reason specified"
                user = warnList[0]
                user = user.replace("<", "")
                user = user.replace("@", "")
                user = user.replace("!", "")
                user = user.replace(">", "")
                pingUser = client.get_user(int(user))
                pingMember = message.guild.get_member(int(user))
                db = cluster["cases"]
                collection = db[str(message.channel.guild.id)]
                numberOfCases = collection.count()
                id = round((datetime.now(timezone.utc) + timedelta(days=0)).timestamp() * 1000000 - 1593028107000000)
                result = {"_id": id, "case-id": numberOfCases+1, "case-type": "mute", "user": str(user),
                          "reason": reason, "moderator": str(message.author)}
                collection.insert_one(result)
                try:
                    await postCase(message, result)
                except:
                    pass
                try:
                    mutedrole = 0
                    for i in message.channel.guild.roles:
                        if i.name == "Muted":
                            mutedrole = i
                    if mutedrole == 0:
                        perms = discord.Permissions()
                        perms.update(send_messages=False, speak=False, send_tts_messages=False)
                        mutedrole = await message.channel.guild.create_role(name="Muted", permissions=perms,
                                                                            color=discord.Colour(0x1b1b1b))
                        await message.channel.send(
                            "Event Horizon did not detect a muted role in your server, so it created one for you.")
                    for channel in message.channel.guild.channels:
                        await channel.set_permissions(mutedrole, send_messages=False, speak=False, send_tts_messages=False)
                    await pingMember.add_roles(mutedrole)
                    embed = discord.Embed(title="**Punishment**",
                                          description="**You have been muted from "+str(message.channel.guild)+". Reason: "+reason+".**", color=0xff0000)
                    await pingUser.send(embed=embed)
                    embed=discord.Embed(title="\✅ ***Case "+str(numberOfCases+1)+": "+str(pingUser)+" has been muted. Reason: "+reason+"***", color=random.randint(0, 0xffffff))
                    await message.channel.send(embed=embed)
                except:
                    mutedrole = 0
                    for i in message.channel.guild.roles:
                        if i.name == "Muted":
                            mutedrole = i
                    if mutedrole == 0:
                        perms = discord.Permissions()
                        perms.update(send_messages=False, speak=False, send_tts_messages=False)
                        mutedrole = await message.channel.guild.create_role(name="Muted", permissions=perms,
                                                                            color=discord.Colour(0x1b1b1b))
                        await message.channel.send(
                            "Event Horizon did not detect a muted role in your server, so it created one for you.")
                    for channel in message.channel.guild.channels:
                        await channel.set_permissions(mutedrole, send_messages=False, speak=False,
                                                      send_tts_messages=False)
                    await pingMember.add_roles(mutedrole)
                    embed = discord.Embed(title="\✅ ***Case " + str(numberOfCases + 1) + ": " + str(
                        pingUser) + " has been muted. Reason: " + reason + "***",
                                          color=random.randint(0, 0xffffff))
                    await message.channel.send(embed=embed)
            else:
                await message.channel.send("You do not have the proper permissions to execute this command.")
    except Exception as exceptz:
        try:
            await message.channel.send("An error occurred! "+str(exceptz)+" For the correct usage, simply type a command without any parameters.")
        except:
            pass


@client.event
async def on_member_join(member):
    try:
        preferences = cluster["preferences"]
        serverID = preferences[str(member.guild.id)]
        resultList = []
        results = serverID.find({})
        for result in results:
            resultList = result
        if 'join-age' in resultList:
            joinAge = resultList['join-age']
            id = round((datetime.now(timezone.utc) + timedelta(days=0)).timestamp())
            if (id - member.created_at.timestamp())/86400 > joinAge:
                try:
                    embed=discord.Embed(title="Kicked from **"+str(member.guild.name)+"**", description="**"+str(member.guild.name)+"** is protected by Event Horizon. Your account is not old enough to be in this server. As a result, you have been kicked. Thank you for understanding.", color=0xff0000)
                    await member.send(embed=embed)
                except:
                    pass
                await member.guild.kick(member)
                preferences = cluster["preferences"]
                preference = preferences[str(member.guild.id)]
                j = ""
                results = preference.find({"mod-channel": {"$exists": False}})
                if results.count() == 0:
                    results = preference.find({})
                    for m in results:
                        j = m
                        modchannel = int(j['mod-channel'])
                    modchannel = client.get_channel(modchannel)
                    embed = discord.Embed(title="Automod", description=str(member)+" was kicked for being too young!", color=random.randint(0, 0xffffff))
                    await modchannel.send(embed=embed)
    except:
        pass

@client.event
async def on_voice_state_update(member, before, after):
    beforec = before.channel
    afterc = after.channel
    preferences = cluster["preferences"]
    serverID = preferences[str(member.guild.id)]
    resultList = []
    results = serverID.find({})
    for result in results:
        resultList = result
    if 'vc-roles' in resultList:
        vcRoles = resultList['vc-roles']
        print(vcRoles)
        for i in vcRoles:
            if before.channel == None:
                if str(after.channel.id) == i:
                    roles = vcRoles[str(after.channel.id)]
                    for i in roles:
                        role = discord.utils.get(member.guild.roles, id=int(i))
                        try:
                            await member.add_roles(role)
                        except:
                            pass
            elif after.channel == None:
                if str(before.channel.id) == i:
                    roles = vcRoles[str(before.channel.id)]
                    for i in roles:
                        role = discord.utils.get(member.guild.roles, id=int(i))
                        try:
                            await member.remove_roles(role)
                        except:
                            pass
            else:
                if str(before.channel.id) == i and str(after.channel.id) != i:
                    roles = vcRoles[str(before.channel.id)]
                    for i in roles:
                        role = discord.utils.get(member.guild.roles, id=int(i))
                        try:
                            await member.remove_roles(role)
                        except:
                            pass
                if str(before.channel.id) != i and str(after.channel.id) == i:
                    roles = vcRoles[str(after.channel.id)]
                    for i in roles:
                        role = discord.utils.get(member.guild.roles, id=int(i))
                        try:
                            await member.add_roles(role)
                        except:
                            pass

@client.event
async def on_guild_join(guild):
    if len(guild.channels) > 0:
        resulte=0
        teste = 0
        introembed = discord.Embed(title="Thank you for adding Event Horizon!", description="This is a multi-purpose bot with moderation and more!\nIf you have added Event Horizon to your server for the first time, admin commands are reserved to any user in the server who has the administrator property. However, you can change this. Other settings can be found in the help menu. \n**The prefix for this bot is: h!**\n To get started, type `h!help`!\n Again, thank you for adding the bot!")
        introembed.set_footer(text="Made with 🔨 by eddyzow#0001 | Event Horizon v1.0.2")
        while resulte == 0:
            try:
                await guild.channels[teste].send(embed=introembed)
                resulte=1
            except:
                teste+=1
                pass


@client.event
async def on_ready():
    print('Bot logged in as')
    print(client.user.name)
    game = discord.Game("h!help")
    await client.change_presence(activity=game)
client.run(str(os.environ.get('BOT_TOKEN')))
