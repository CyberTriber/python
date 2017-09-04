# coding=utf-8
"""
  Discord chatbot by CyberTriber (https://github.com/CyberTriber)

==============================================================
"""
import discord
import asyncio
import random
import pickle
import os

# replace ############### with your bot token
token = '###############'

# place channel owner id here
owner_id = ''

# Put your custom bot name here
bot_name = 'CyberGuard'
bot_version = '1.0'

# choose your custom command prefix (! is default - for !contact, !coin ...)
command_prefix = '!'

# Create a file for storing allowed user to put URLs in chat
if not os.path.isfile('allowurl.pk1'):
    allowURL = list()
else:
    with open('allowurl.pk1', 'rb') as file:
        allowURL = pickle.load(file)


# define bot client
client = discord.Client()

@client.event
async def on_ready():
    print(bot_name+' - version: '+bot_version+' Created by CyberTriber (https://github.com/CyberTriber)')
    print(client.user.name+'( '+client.user.id+' )'' connected')
    
    # allow bot to use URL in chat
    allowURL.append(client.user.id)

    # allow owner to use URL in chat
    allowURL.append(owner_id)

# catch commands from chat
@client.event
async def on_message(message):

    if message.content.startswith(command_prefix+'contact'):
        await client.send_message(message.channel, '#######')   # Replace ####### with your contact info, use \n to new line
                                                                # (www.facebook.com/myname\nwww.youtube.com/myname\nwww.twitter.com/myothername and so on)

    if message.content.startswith(command_prefix+'coin'):
        coin = random.choice(['HEADS','TAILS'])
        await client.send_message(message.channel, 'Tossing coin and result is ... '+coin)

    # allow user to use URL in chat (Use: !allowurl @somecoolguy )
    if message.content.startswith(command_prefix+'allowurl'):
        if message.author.id == owner_id:
            if len(message.mentions) > 0:
                    for user in message.mentions:
                        allowURL.append(user.id)
                        with open('allowurl.pk1', 'wb') as file:
                            pickle.dump(allowURL, file)
                        print(allowURL)
        else:
            await client.send_message(message.channel, 'You are not allowed to use this command')

    # denny user from use URL in chat (Use: !dennyurl @somecoolguy )
    if message.content.startswith(command_prefix+'dennyurl'):
        if message.author.id == owner_id:
            if len(message.mentions) > 0:
                    for user in message.mentions:
                        if (user.id in allowURL):
                            allowURL.remove(user.id)
                            with open('allowurl.pk1', 'wb') as file:
                                pickle.dump(allowURL, file)
                        print(allowURL)
        else:
            await client.send_message(message.channel, 'You are not allowed to use this command')    

    # Delete url messages if posted by ppl who are not allowed to do that
    if (message.content.find('http://') >= 0) or (message.content.find('https://') >= 0):
        if message.author.id not in allowURL:
            await client.send_message(message.channel, 'URLs are blocked, ask admin for permission')
            await client.delete_message(message)

    # print any posted message (except from bot itself) to terminal window (format is User (user_id) - message)
    if message.author.id != client.user.id:
        print(message.author.name+'('+message.author.id+') - '+message.content)

# start bot
client.run(token)