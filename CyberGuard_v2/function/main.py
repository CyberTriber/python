# coding=utf-8
import discord
from discord.ext.commands import Bot
import pyrebase
import os
import time
import datetime
import pickle

from secrets.secrets import *
from commands.user import *

# Discord INIT
botName = 'CyberGuard'
command_prefix = '!'
global client
client = Bot(command_prefix=command_prefix, pm_help=True, case_insensitive=True)
client.login(BOT_TOKEN)

# Settings for pyrebase database
firebase = pyrebase.initialize_app(CONFIG)
auth = firebase.auth()
user = auth.sign_in_with_email_and_password(FBEMAIL, FBPASSWORD)
db = firebase.database()

# Temporaly using allowedURL storing into file (will be moved to database)
if not os.path.isfile('allowurl.pk1'):
    allowURL = list()
else:
    with open('allowurl.pk1', 'rb') as file:
        allowURL = pickle.load(file)



# function for emoji counter (counts emoji in message for filtering)
def getEmojiByName(n,e):
    emoji = list(e)
    for t in emoji:
        if n in t.name:
            return t

# get actual time
def getTime():
    ts = time.time()
    t = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return t

def is_in_db(user_id):
    error = False
    try:
        name = db.child("users").child(user_id).child('name').get().val()
    except:
        error = True
        print("Unexpected error:", sys.exc_info()[0])

    if not error:
        if name:
            return True
        else:
            return False


def setLevel(user_id, newPoints):
    newLevel = 0
    for i in range(1,len(LEVEL_SYSTEM)+1):
	    if newPoints >= LEVEL_SYSTEM.get(i).get('cap'):
	        newLevel = LEVEL_SYSTEM.get(i).get('level')
	        newMultiplier = LEVEL_SYSTEM.get(i).get('multiplier')

    db.child("users").child(user_id).update({'level': newLevel})
    db.child("users").child(user_id).update({'multiplier': newMultiplier})
