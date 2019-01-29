import discord
from datetime import datetime
import math
from math import floor
import time
import asyncio
import os
import random
repAdder = 0
line = "unsp"
user_search_value = "undef"
client = discord.Client()
count = 0
words = "undef"
authorizedAuthors = ['christmasy eddyzow#9988','Kyle!#2949']
points = 123
repAdder2 = 0
@client.event
async def on_member_join(member):
    global word
    now = (str(datetime.now()))
    now1 =(str(member.created_at))
    now = now.split(' ')
    print(now)
    now1 = now1.split(' ')
    print(now1)
    now = int(str(now[0]).replace('-', ''))
    now1 = int(str(now1[0]).replace('-', ''))
    print(now-now1)
    dayDiff = now-now1
    if dayDiff != 0 and dayDiff != 1 and dayDiff != 2 and dayDiff != 2 and dayDiff != 3 and dayDiff != 4 and dayDiff != 5 and dayDiff != 6 and dayDiff != 7 and dayDiff != 8 and dayDiff != 9 and dayDiff != 10 and dayDiff != 11 and dayDiff != 12 and dayDiff != 13 and dayDiff != 14 and dayDiff != 73 and dayDiff != 74 and dayDiff != 75 and dayDiff != 76 and dayDiff != 77 and dayDiff != 78 and dayDiff != 79 and dayDiff != 80 and dayDiff != 81 and dayDiff != 82 and dayDiff != 83 and dayDiff != 84 and dayDiff != 85 and dayDiff != 86 and dayDiff != 87 and dayDiff != 88 and dayDiff != 89 and dayDiff != 8883 and dayDiff != 8882 and dayDiff != 8881 and dayDiff != 8880 and dayDiff != 8879 and dayDiff != 8878 and dayDiff != 8877 and dayDiff != 8876 and dayDiff != 8875 and dayDiff != 8874 and dayDiff != 8873 and dayDiff != 8872 and dayDiff != 8871 and dayDiff != 8870:
        print(str(member)+' just joined!')
        repAdder = '<@'+str(member.id)+'>'
        user_search_value = str(repAdder)
        count = 0
        with open("repubotdata.txt", 'r') as f:
            for line in f.readlines():
                words = line.lower().split()
                for word in words:
                    if word == user_search_value:
                        count += 1
                    if word == "-" + str(user_search_value):
                        count -= 1
                word = word.replace('!', '')
                print(count)
        user = member
        if count > 19:
            role = discord.utils.get(user.server.roles, name='Trusted')
            await client.add_roles(user, role)
        if count < 20:
            role = discord.utils.get(user.server.roles, name='Trusted')
            await client.remove_roles(user, role)
        if count < 0:
            role = discord.utils.get(user.server.roles, name='Negative Rep')
            await client.add_roles(user, role)
        if count > -1:
            role = discord.utils.get(user.server.roles, name='Negative Rep')
            await client.remove_roles(user, role)
        if count < -14:
            role = discord.utils.get(user.server.roles, name='Troll (-15 Points)')
            await client.add_roles(user, role)
            role = discord.utils.get(user.server.roles, name='Member')
            await client.remove_roles(user, role)
        if count > -15:
            role = discord.utils.get(user.server.roles, name='Troll (-15 Points)')
            await client.remove_roles(user, role)
        if count > 49:
            role = discord.utils.get(user.server.roles, name='Legend')
            await client.add_roles(user, role)
        if count < 50:
            role = discord.utils.get(user.server.roles, name='Legend')
            await client.remove_roles(user, role)
        if count > 29:
            role = discord.utils.get(user.server.roles, name='Master')
            await client.add_roles(user, role)
        if count < 30:
            role = discord.utils.get(user.server.roles, name='Master')
            await client.remove_roles(user, role)
        if count > 19:
            role = discord.utils.get(user.server.roles, name='Trusted')
            await client.add_roles(user, role)
        if count < 20:
            role = discord.utils.get(user.server.roles, name='Trusted')
            await client.remove_roles(user, role)
        if count < 0:
            role = discord.utils.get(user.server.roles, name='Negative Rep')
            await client.add_roles(user, role)
        if count > -1:
            role = discord.utils.get(user.server.roles, name='Negative Rep')
            await client.remove_roles(user, role)
        if count < -14:
            role = discord.utils.get(user.server.roles, name='Troll (-15 Points)')
            await client.add_roles(user, role)
            role = discord.utils.get(user.server.roles, name='Member')
            await client.remove_roles(user, role)
        if count > -15:
            role = discord.utils.get(user.server.roles, name='Troll (-15 Points)')
            await client.remove_roles(user, role)
        if count > 49:
            role = discord.utils.get(user.server.roles, name='Legend')
            await client.add_roles(user, role)
        if count < 50:
            role = discord.utils.get(user.server.roles, name='Legend')
            await client.remove_roles(user, role)
        if count > 29:
            role = discord.utils.get(user.server.roles, name='Master')
            await client.add_roles(user, role)
        if count < 30:
            role = discord.utils.get(user.server.roles, name='Master')
            await client.remove_roles(user, role)
    else:
        banner = member
        try:
            await client.send_message(member, 'Your account has been detected to be an alt. If this is in error please wait a couple days and try to join again.')
        except:
            pass
        await client.kick(banner)

    
        
        
            

@client.event
async def on_ready():
    print('Bot logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(str(os.environ.get('BOT_TOKEN')))
