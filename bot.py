import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import random
import requests
import os
repAdder = 0
line = "unsp"
user_search_value = "undef"
found = "unsp"
client = discord.Client()
count = 0
words = "undef"
authorizedAuthors = ['christmasy eddyzow#9988','Kyle!#2949']
points = 123
repAdder2 = 0
@client.event
async def on_message(message):
    global repAdder
    global points
    global authorizedAuthors
    global user_search_value
    global count
    global line
    global words
    global repAdder2
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!rep add'):
        param, repAdder = message.content.split("rep add ",1)
        if "<@!"+message.author.id+">" != repAdder and "<@"+message.author.id+">" != repAdder:
            f = open("repubotdata.txt","a")
            f.write(' '+repAdder+' ',)
            f.close()
            user_search_value = str(repAdder)
            count = 0    
            with open("repubotdata.txt", 'r') as f:
                for line in f.readlines():
                    words = line.lower().split()
                    print(words)
                    for word in words:
                        if word == user_search_value:
                            count += 1
                    msg = str(message.author)+', given '+repAdder+' **1** reputation point. They now have '+str(count)+' points'
                    await client.send_message(message.channel, msg)
        else:
            msg = repAdder+" Sorry, you cannot give yourself points!"
            await client.send_message(message.channel, msg)
    if message.content.startswith('!rep rem'):
        param, repAdder = message.content.split("rep rem ",1)
        if "<@!"+message.author.id+">" != repAdder:
            user_search_value = str(repAdder)
            count = 0    
            with open("repubotdata.txt", 'r') as f:
                 for line in f.readlines():
                    words = line.lower().split()
                    print(words)
                    print(user_search_value)
                    words.remove(user_search_value)
                    words = ' '.join(words)
                    print(words)
            f = open("repubotdata.txt","w")
            f.write(str(words))
            f.close()
            with open("repubotdata.txt", 'r') as f:
                for line in f.readlines():
                    words = line.lower().split()
                    print(words)
                    for word in words:
                        if word == user_search_value:
                            count += 1
                    msg = str(message.author)+', taken **1** reputation point from '+repAdder+'. They now have '+str(count)+' points'
                    await client.send_message(message.channel, msg)
        else:
            msg = repAdder+" You cannot take points from yourself!"
            await client.send_message(message.channel, msg)
    if message.content.startswith('!staff ra'):
        if message.author in authorizedAuthors:
            param, repAdder = message.content.split("staff ra ",1)
            print(repAdder)
    if message.content.startswith('!points'):
        param, repAdder = message.content.split("points ",1)
        user_search_value = str(repAdder)
        count = 0    
        with open("repubotdata.txt", 'r') as f:
            for line in f.readlines():
                words = line.lower().split()
                for word in words:
                    if word == user_search_value:
                        count += 1
                msg = 'This user has '+str(count)+' points'
                await client.send_message(message.channel, msg)

    
        
        
            

@client.event
async def on_ready():
    print('Bot logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(str(os.environ.get('BOT_TOKEN')))
