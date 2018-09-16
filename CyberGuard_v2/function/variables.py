# coding=utf-8

global DEBUG_ON		# Turn debug ON/OF (True/False)
DEBUG_ON = False

global LEVEL_SYSTEM	# Settings for leveling system
LEVEL_SYSTEM = {
	'1': {'cap': 0, 'multiplier': 1},
	'2': {'cap': 10, 'multiplier': 1},
	'3': {'cap': 100, 'multiplier': 2},
	'4': {'cap': 500, 'multiplier': 2},
	'5': {'cap': 1000, 'multiplier': 3},
	'6': {'cap': 2000, 'multiplier': 3},
	'7': {'cap': 5000, 'multiplier': 3},
	'8': {'cap': 10000, 'multiplier': 4},
	'8': {'cap': 20000, 'multiplier': 5}
}

global NEW_USER		# Default settings for new users
NEW_USER = {
	'credit': 100,
	'points': 0,
	'level': 1,
	'multiplier': 1,
	'xp': 0,
	'weapons': {},
	'active_weapon': ''
}

# Info screen settings
global INFO_BG
global EMPTY_AVATAR
global INFO_BG1
global FONT1
global FONT2
global FONT3
global FONT4
global STATUS_COLORS

INFO_BG = './static/img/bg.png'					# base background of info graphic
INFO_BG1 = './static/img/bg1.png'				# left part covering avatar and make them rounded
EMPTY_AVATAR = './static/img/no_avatar.png'		# default picture for users without avatar

FONT1 = './static/fonts/Ignis et Glacies Sharp.ttf'
FONT2 = './static/fonts/GFSNeohellenicBold.ttf'
FONT3 = '/usr/share/fonts/truetype/freefont/FreeSans.ttf'

STATUS_COLORS={
    'online': (67, 181, 129),
    'offline': (116, 127, 141),
    'idle': (250, 166, 26),
    'dnd': (240, 71, 71),
    'invisible': (116, 127, 141)}

