# coding=utf-8
from function.main import *
from function.variables import *
from secrets.secrets import *
import pickle
import asyncio


@client.command(pass_context=True)
@discord.ext.commands.has_role('@CyberMachine')
async def allowurl(ctx, user):
    if len(ctx.message.mentions[0].name) > 0:
        allowURL.append(ctx.message.mentions[0].id)
        with open('allowurl.pk1', 'wb') as file:
            pickle.dump(allowURL, file)
        #print(allowURL)
    else:
        await client.say(ctx.message.author.name+' specify user to add URL permission')


@client.command(pass_context=True)
@discord.ext.commands.has_role('@CyberMachine')
async def denyurl(ctx, user):
    if len(ctx.message.mentions[0].name) > 0:
        if (ctx.message.mentions[0].id in allowURL):
            allowURL.remove(ctx.message.mentions[0].id)
            with open('allowurl.pk1', 'wb') as file:
                pickle.dump(allowURL, file)
        #print(allowURL)
    else:
        await client.say(ctx.message.author.name+' specify user to remove URL permission')

@client.command(pass_context=True)
@discord.ext.commands.has_role('@CyberMachine')
async def urlinfo(ctx):
    await client.say('This users are allowed to send URLs:')
    for i in allowURL:
        #u = await client.say(client.get_user_info(i))
        hi = await client.get_user_info(i)
        await client.say(hi.name)
        await asyncio.sleep(1)

@client.command(pass_context=True)
@discord.ext.commands.has_role('@CyberMachine')
async def clear(ctx, par: int):
    msg = []
    num = par + 1
    async for x in client.logs_from(ctx.message.channel, limit = num):
        msg.append(x)
    try:
        await client.delete_messages(msg)
    except Exception as e:
        error = True
        if DEBUG:
            print(e)
        else:
            await client.say('OOPS something\'s wrong, contact CyberTriber for more info')
            print(getTime()+"\tUnexpected error:", sys.exc_info()[0])

@client.command(pass_context=True)
@discord.ext.commands.has_role('@CyberMachine')
async def clearall(ctx):
    msg = []
    num = 100 #max amount of bulk messages that can be deleted set by discord
    async for x in client.logs_from(ctx.message.channel, limit = num):
        msg.append(x)
    #print (msg)
    try:
        await client.delete_messages(msg)
    except Exception as e:
        error = True
        if DEBUG:
            print(e)
        else:
            await client.say('OOPS something\'s wrong, contact CyberTriber for more info')
            print(getTime()+"\tUnexpected error:", sys.exc_info()[0])

@client.command(pass_context=True)
@discord.ext.commands.has_role('@CyberMachine')
async def adduser(ctx, user: discord.Member):
    data = {}
    startCredit = 0
    test = None
    error = False

    if is_in_db(user.id):
        await client.say(user.name+' is in our database already')
    else:
        data.update(name=user_name)
        data.update(id=userid)
        data.update(credit=NEW_USER.get('credit'))
        data.update(points=NEW_USER.get('points'))
        data.update(level=NEW_USER.get('level'))
        data.update(multiplier=NEW_USER.get('multiplier'))
        data.update(xp=NEW_USER.get('xp'))
        data.update(weapons=NEW_USER.get('weapons'))
        data.update(active_weapon=NEW_USER.get('active_weapon'))
        try:
            db.child("users").child(user.id).set(data)
        except Exception as e:
            error = True
            if DEBUG:
                print(e)
            else:
                await client.say('OOPS something\'s wrong, contact CyberTriber for more info')
                print(getTime()+"\tUnexpected error:", sys.exc_info()[0])
        
        if not error:
            await client.say(user.name+' has been successfuly added to our database')

@client.listen('on_message')
async def on_message(message):
    emojis = client.get_all_emojis()
    if message.author.id != client.user.id:
        print(getTime()+'\t'+message.author.name+'('+message.author.id+') - '+message.content)
        if 'cyber' in message.content or 'Cyber' in message.content:
            await client.add_reaction(message, getEmojiByName('heart', emojis))
        if 'bot' in message.content or 'Bot' in message.content:
            await client.add_reaction(message, getEmojiByName('robotface_01', emojis))

        error = False
        try:
            points = db.child("users").child(message.author.id).child('points').get().val()
            level = db.child("users").child(message.author.id).child('level').get().val()
            multiplier = db.child("users").child(message.author.id).child('multiplier').get().val()
        except Exception as e:
            error = True
            if DEBUG:
                print(e)
            else:
                await client.say('OOPS something\'s wrong, contact CyberTriber for more info')
                print(getTime()+"\tUnexpected error:", sys.exc_info()[0])

        if not error:
            if is_in_db(message.author.id):
                try:
                    oldPoints = db.child("users").child(message.author.id).child('points').get().val()
                    multiplier = db.child("users").child(message.author.id).child('multiplier').get().val()
                    level = db.child("users").child(message.author.id).child('level').get().val()
                except Exception as e:
                    error = True
                    if DEBUG:
                        print(e)
                    else:
                        await client.say('OOPS something\'s wrong, contact CyberTriber for more info')
                        print(getTime()+"\tUnexpected error:", sys.exc_info()[0])

                if not error:
                    newPoints = oldPoints + (multiplier * 1) + 1
                    db.child("users").child(message.author.id).child('points').set(newPoints)
                    setLevel(message.author.id, newPoints)

    if (message.content.find('http://') >= 0) or (message.content.find('https://') >=0 ) or (message.content.find('www.') >= 0):
        if message.author.id not in allowURL:
            await client.send_message(message.channel, 'You have no permission to post URLs, ask admins for higher priviledges')
            await client.delete_message(message)