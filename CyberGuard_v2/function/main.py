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

def poll_exist(user_id):
    error = False
    try:
        getID = db.child('poll').child(user_id).child('created').get().val()
    except:
        error = True
        print("Unexpected error:", sys.exc_info()[0])

    if not error:
        if getID is not None:
            return True
        else:
            return False


def create_poll(user_id, data):
    error = False
    print(str(data))
   
    print(getTime()+'\t [DEBUG] - '+'create_poll funct:')
    try:
        db.child('poll').child(user_id).set(data)
    except:
        error = True
        print("Unexpected error:", sys.exc_info()[0])

def read_poll(user_id):
    error = False
    pollData={}
    try:
        question = db.child('poll').child(user_id).child('question').get().val()
        answers = db.child('poll').child(user_id).child('answers').get().val()
        created = db.child('poll').child(user_id).child('created').get().val()
        time = db.child('poll').child(user_id).child('time').get().val()
        results = db.child('poll').child(user_id).child('results').get().val()
        expire = db.child('poll').child(user_id).child('expire').get().val()
    except:
        error = True
        print("Unexpected error:", sys.exc_info()[0])        

    if not error:
        pollData = {'question': question, 'answers': answers, 'created': created, 'time': time, 'results': results, 'expire': expire}
        print(getTime()+'\t [DEBUG] - '+str(pollData))
    else:
        pollData = {}
    return pollData

def setLevel(user_id, newPoints):
    newLevel = 0
    if newPoints >= 10:
        newLevel = 2
        newMultiplier = 2

    if newPoints >= 100:
        newLevel = 3
        newMultiplier = 3

    if newPoints >= 500:
        newLevel = 4
        newMultiplier = 4

    if newPoints >= 1000:
        newLevel = 5
        newMultiplier = 5

    if newPoints >= 2000:
        newLevel = 6
        newMultiplier = 6

    if newPoints >= 5000:
        newLevel = 7
        newMultiplier = 7

    db.child("users").child(user_id).update({'level': newLevel})
    db.child("users").child(user_id).update({'multiplier': newMultiplier})

	# Level 1 - 0..10 points (multiplier: 1)
	# Level 2 - 10..100 points (multiplier: 2)
	# Level 3 - 100..500 points (multiplier: 3)
	# Level 4 - 500..1000 points (multiplier: 4)
	# Level 5 - 1000..2000 points (multiplier: 5)
	# Level 6 - 2000..5000 points (multiplier: 6)
	# Level 7 - 5000+ points (multiplier: 7)