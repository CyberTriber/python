# coding=utf-8
"""
  Discord chatbot by CyberTriber (https://github.com/CyberTriber)
  version: 2.0.0

==============================================================
"""

from secrets.secrets import *			# Import secret info for discord and firebase login
from commands.user import *				# Import commands for users
from commands.admin import *			# Import commands for admins


def dprint(data):
	if DEBUG:
		print(getTime()+'\t [DEBUG] - '+data)

def startBot():
	client.run(BOT_TOKEN)

if __name__ == '__main__':
	startBot()