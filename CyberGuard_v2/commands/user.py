# coding=utf-8
from function.main import *
from function.variables import *
from secrets.secrets import *
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from io import BytesIO
import requests
import shutil
import time
import datetime
import asyncio

start = getTime()

@client.event
async def on_ready():
	print('\033c')
	print(botName+' - version: 2.0 Created by CyberTriber (https://github.com/CyberTriber)')
	print(client.user.name+'( '+client.user.id+' )'' is successfuly connected (at '+start+')')
	print('-------------------------------------------------------------------------------')
	# add itself and owner to allowURL list
	allowURL.append(client.user.id)
	allowURL.append(OWNER_ID)

	await client.change_presence(game=discord.Game(name="CyberCity", type=3))

	async def list_servers():
		#await client.wait_until_ready()
		while not client.is_closed:
			print("Current servers:")
			for server in client.servers:
				print(server.name)
			print('\n\nServer log:')
			await asyncio.sleep(600)

	client.loop.create_task(list_servers())


# Display Top 10 most active users (by points)
@client.command(pass_context=True, brief='Top 10 most active users (by points)')
@discord.ext.commands.has_role('@Android')
async def topten(ctx):
	error = False
	std = []
	try:
		user_list = db.child("users").get()
		for i in user_list.each():
			item = i.val()
			std.append((item.get('name'),item.get('points')))

		def takeSecond(elem):
			return elem[1]

		std.sort(key=takeSecond,reverse=True)

	except Exception as e:
		error = True
		if DEBUG:
			print(e)
		else:
			await client.say('OOPS something\'s wrong, contact CyberTriber for more info')
			print("Unexpected error:", sys.exc_info()[0])
		

	if not error:
		embed = discord.Embed(title = 'TOPTEN (by points)', color = 0x00ff00)
		pos = 1
		l = ''
		for it in std:
			if pos < 11:
				l += str(pos)+'.  '+it[0]+" ("+str(it[1])+")\n"
				pos += 1
		embed.add_field(name = l, value = '⠀', inline = False)
		await client.say(embed=embed)

# Display info about user
@client.command(pass_context=True, brief='Display info about you or any user on this server')
@discord.ext.commands.has_role('@Android')
async def info(ctx,  user=''):
	error = False
	if user == '':
		user = ctx.message.author
	else:
		user = ctx.message.mentions[0]

	if is_in_db(user.id):
		try:
			balance = str(db.child("users").child(user.id).child('credit').get().val())
			points = str(db.child("users").child(user.id).child('points').get().val())
			level = str(db.child("users").child(user.id).child('level').get().val())
			multiplier = str(db.child("users").child(user.id).child('multiplier').get().val())
			xp = str(db.child("users").child(user.id).child('xp').get().val())
			role = str(user.top_role)
			joined = user.joined_at.strftime('%Y-%m-%d %H:%M:%S')
			status = str(user.status)
			level_cap={'0': 1,'1': 1, '2': 10, '3': 100, '4': 500, '5': 1000, '6': 2000, '7': 5000}
			color = STATUS_COLORS.get(status)
			t = datetime.datetime.strptime(str(user.joined_at), '%Y-%m-%d %H:%M:%S.%f')
			e = (t - datetime.datetime(1970, 1, 1)).total_seconds()
			joined = datetime.datetime.fromtimestamp(e).strftime('%Y-%m-%d %H:%M:%S')

		except Exception as e:
			error = True
			if DEBUG:
				print(e)
			else:
				await client.say('OOPS something\'s wrong, contact CyberTriber for more info')
				print(getTime()+"\tUnexpected error:", sys.exc_info()[0])
		
		if not error:

			avatar_img = EMPTY_AVATAR
			avatar_url = (user.avatar_url).replace('.webp?size=1024','.png')
			try:
				response = requests.get(avatar_url, stream=True)
				with open('img.png', 'wb') as out_file:
					shutil.copyfileobj(response.raw, out_file)
				del response
				avatar_img = "img.png"
			except:
				avatar_img = EMPTY_AVATAR
			finally:
				
				im = Image.open(INFO_BG)

				avatar = Image.open(avatar_img)

				avatar = avatar.resize((160,160), Image.ANTIALIAS)
				# print(avatar.format, avatar.size, avatar.mode)
						
				mask = Image.open(INFO_BG1)

				im.paste(avatar, (15,15), mask=avatar)
				im.paste(mask, (0,0), mask=mask)

				draw = ImageDraw.Draw(im)

				font1 = ImageFont.truetype(FONT1, 32)
				font2 = ImageFont.truetype(FONT2, 18)
				font3 = ImageFont.truetype(FONT2, 24)
				font4 = ImageFont.truetype(FONT3,18)

				x = 200
				x1 = x+140
				y = 25

				fill = u"\u25A0"
				empty = u"\u25A1"

				namePos_shadow = (x+3,y-2)
				namePos = (x,y-5)

				levelPos = (x,y+35)
				level_valPos = (x+50,y+40)
				progress_testPos = ()
				progress_barPos = (x1,y+35)

				rolePos = (x,y+60)
				role_valPos = (x1,y+62)

				pointsPos = (x,y+85)
				points_valPos = (x+60,y+90)
				creditPos = (x1,y+85)
				credit_valPos = (x1+60,y+90)

				xpPos = (x,y+110)
				xp_valPos = (x+30,y+115)
				joinedPos = (x1,y+110)
				joined_valPos = (x1+60,y+115)

				statusPos = (250,75)
				status_valPos = (250,100)

				if is_in_db(ctx.message.author.id):
					try:
						curPoints = int(points)
						lvl = int(level)
					except Exception as e:
						error = True
						if DEBUG:
							print(e)
						else:
							await client.say('OOPS something\'s wrong, contact CyberTriber for more info')
							print(getTime()+"\tUnexpected error:", sys.exc_info()[0])

					if not error:
						cap = level_cap[str(lvl+1)]
						barF = int(10*curPoints/cap)
						barE = 10 - barF
				else:
					print('you are not in DB')

				if barF < 1:
					bar = 10*empty
				else:
					bar = barF*fill+barE*empty

				draw.text(namePos_shadow,user.name,(20,20,20),font=font1)
				draw.text(namePos,user.name,(84,171,237),font=font1)

				draw.text(level_valPos,level,(84,171,237),font=font2)
				draw.text(levelPos,"level",(255,255,255),font=font3)
				draw.text(progress_barPos,bar,(255,255,255),font=font4)

				draw.text(rolePos,'highest role',(255,255,255),font=font3)
				draw.text(role_valPos,role,(84,171,237),font=font2)

				draw.text(pointsPos,"points",(255,255,255),font=font3)
				draw.text(points_valPos,points,(84,171,237),font=font2)
				draw.text(creditPos,"credits",(255,255,255),font=font3)
				draw.text(credit_valPos,balance,(84,171,237),font=font2)

				draw.text(xpPos,"xp",(255,255,255),font=font3)
				draw.text(xp_valPos,xp,(84,171,237),font=font2)
				draw.text(joinedPos,"joined",(255,255,255),font=font3)
				draw.text(joined_valPos,joined,(84,171,237),font=font2)

				draw.ellipse((115, 128, 145, 158), fill = color, outline = color)

				#im.show()
				im.thumbnail((400,133), Image.ANTIALIAS)
				buffer = BytesIO()
				im.save(buffer, "PNG")
				buffer.seek(0)
				await client.send_file(ctx.message.channel, buffer, filename="info.png") 
		else:
			await client.say('user is not in database')

# Command for users to add them to database
@client.command(pass_context=True, brief='Adds you into our database')
@discord.ext.commands.has_role('@Android')
async def addme(ctx):
	"""
	Adds you into our database, allows you to use build in economy system and track your stats
	"""
	data = {}
	user_name = ctx.message.author.name
	user_id = ctx.message.author.id
	error = False
	if is_in_db(user_id):
		await client.say(user_name+' you are in our database already')
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
			db.child("users").child(id).set(data)
		except Exception as e:
			error = True
			if DEBUG:
				print(e)
			else:
				await client.say('OOPS something\'s wrong, contact CyberTriber for more info')
				print(getTime()+"\tUnexpected error:", sys.exc_info()[0])
		
		if not error:
			await client.say(user_name+' has been successfuly added to our database, as a thank we gave you 100 credits')

# Allow user to send credits to another user
@client.command(pass_context=True)
@discord.ext.commands.has_role('@Android')
async def give(ctx, us: discord.Member, am: int):
	error = False
	newBalance1 = 0
	newBalance2 = 0
	getCredit1 = db.child("users").child(ctx.message.author.id).child('credit').get().val()
	getCredit2 = db.child("users").child(us.id).child('credit').get().val()
	if am < 0:
		await client.say('You can\'t send negative amount!')
	else:
		if is_in_db(us.id):
			if getCredit1 >= am:
				newBalance1 = getCredit1 - am
				newBalance2 = getCredit2 + am
				#print('newBalance1: '+str(newBalance1)+', newBalance2: '+str(newBalance2))
				try:
					db.child("users").child(ctx.message.author.id).child('credit').set(newBalance1)
					db.child("users").child(us.id).child('credit').set(newBalance2)
				except:
					error = True
					await client.say('OOPS something\'s wrong, contact CyberTriber for more info')
					print("Unexpected error:", sys.exc_info()[0])

				if not error:
					print(getTime()+'\t'+ctx.message.author.name+' will give '+str(am)+' to '+us.name+' he has now '+str(newBalance1)+' credits.')
					await client.say(ctx.message.author.name+' sent to '+us.name+' '+str(am)+' credits.')
			else:
					await client.say(ctx.message.author.name+' you don\'t have enough credits.')
		else:
			await client.say(us.name+' isn\'t in database')

# Get avatar
@client.command(pass_context=True)
@discord.ext.commands.has_role('@Android')
async def avatar(ctx, user=''):
	if user == '':
		user = ctx.message.author
	else:
		user = ctx.message.mentions[0]

	embed = discord.Embed(title = 'Avatar for '+user.name, color = 0x123654)
	embed.set_image(url=user.avatar_url)
	embed.add_field(name = "AvatarURL:", value = '[Open in browser]('+user.avatar_url+')' , inline = True)
	await client.say(embed=embed)

