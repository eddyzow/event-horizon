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
async def on_message(message):
    try:
        if str(message.mentions[0].id) == '539559376277471291':
            await client.send_message(message.channel, 'Hey! Who pinged me?')
    except:
        pass
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
    else:
        banner = member
        try:
            await client.send_message(member, 'Your account has been detected to be an alt. If this is in error please wait a couple days and try to join again.')
        except:
            pass
        print(str(member)+' just got kicked!')
        await client.kick(banner)

    
        
        
            

@client.event
async def on_ready():
    print('Bot logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(str(os.environ.get('BOT_TOKEN')))
