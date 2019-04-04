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
allowedUsers = []
user_search_value = "undef"
client = discord.Client()
count = 0
kicked = 0
words = "undef"
authorizedAuthors = ['eddyzow#0001','Kyle!#2949']
points = 123
repAdder2 = 0
@client.event
async def on_message(message):
    global kicked
    await client.change_presence(game=discord.Game(name='Kicked '+str(kicked)+' alt accounts!'))
    try:
        if str(message.mentions[0].id) == '539559376277471291':
            await client.send_message(message.channel, 'Hey! Who pinged me?')
    except:
        pass
    if message.content.startswith('s/allow '):
        authorizedAuthors = ['eddyzow#0001', 'Kyle!#2949', 'NewJerichoMan#8571', 'PopeRobXXIII#2197', 'Cameron#7335', 'Tom#2603', 'Sakaya Rito#4853', 'Mtnz#3555', 'moneill6720#7862', 'MrCandy#2119']
        if str(message.author) in authorizedAuthors:
			param, term = message.content.split('s/allow ')
			allowedUsers.append(str(term)
			await client.send_message(message.channel, term+' has been allowed!')
            
@client.event
async def on_member_join(member):
    global kicked
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
	elif str(member) in allowedUsers:
		print(str(member)+' was allowed into the server')
    else:
        banner = member
        try:
            await client.send_message(member, 'Your account has been detected to be an alt. If this is in error please wait a couple days and try to join again.')
        except:
            pass
        print(str(member)+' just got kicked!')
        kicked += 1
        await client.kick(banner)

    
        
        
            

@client.event
async def on_ready():
    print('Bot logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(str(os.environ.get('BOT_TOKEN')))
