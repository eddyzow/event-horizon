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

async for guild in client.fetch_guilds(limit=150):
    print(guild.name)

@client.event
async def on_message(message):
    global kicked
    if str(os.environ.get('keyword1')) in str(message.content) and str(os.environ.get('keyword2')) in str(message.content).lower():
    	bh = client.get_guild(int(os.environ.get(si)))
    	await bh.ban(message.author, delete_message_days=7)
    try:
        if str(message.mentions[0].id) == 539559376277471291:
            await message.channel.send('Hey! Who pinged me?')
    except:
        pass
    if message.content.startswith('s/allow '):
        authorizedAuthors = ['eddyzow#0001']
        if str(message.author) in authorizedAuthors: 
            param, term = message.content.split('s/allow ')
            allowedUsers.append(str(term))
            await message.channel.send(term+' has been allowed! They will be removed again in 1 minute. Please let them join now.')
            time.sleep(60)
            allowedUsers.remove(str(term))
            await message.channel.send(str(term)+' has been re-denied! To add them again, just re-type the command.')
            
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
	    print(allowedUsers)
	    print(str(member)+' was allowed into the server')
    else:
        banner = member
        try:
            await member.send('Your account has been detected to be a new account. New accounts are not allowed to join this server. Please wait a couple days and try to join again.')
        except:
            pass
        print(str(member)+' just got kicked!')
        kicked += 1
        await member.guild.kick(member)

    
        
        
            

@client.event
async def on_ready():
    print('Bot logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(str(os.environ.get('BOT_TOKEN'))) 
 
