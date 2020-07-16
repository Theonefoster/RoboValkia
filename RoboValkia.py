# -*- coding: utf-8 -*-
import random
import re
import requests

from threading     import Thread
from time          import time, sleep, localtime
from os            import path
from datetime      import datetime, date
from contextlib    import suppress

from chatbot       import ChatBot
from credentials   import bot_name, password, channel_name, authorisation_header
from API_functions import get_subscribers, get_youtube_sub_count
from fortunes      import fortunes
#from subscribers   import subs

mods = {'valkia', 'zukesr', 'dogofwar_', 'sir_to_you', 'fiveub', 'mrsamkim', 'stodeh', 'phasegames', 'moobot', 
		'gfox_1', 'onscreen', 'valkiabud', 'monstercat', 'shiveringsoldier', 'pugthepanda', 'overwatchcentral', 
		'giibbayy', 'skywardtheyflew', 'magmayaes', 'mauville', 'purplefoxog', 'ohbot', 'streamlabs', 'sips_', 
		'pearcen', 'ryancentral', 'revlobot', 'kartoonkrazy', 'mettaa_', 'powahline', 'techuman', 'streamelements', 
		'viliqqu', 'ltcoolerooney', 'zetecx', 'adogth1rt3en', 'saltystallion', 'templar9206', 'narpt', 'maddihunt', 
		'solaris0', 'wavow', 'manishade', 'puzzlinggames', 'tompdb', 'mauviiie', 'racheleanne', 'chayonnaise', 
		'horizonsun__', 'jasonkaplan', 'holiwhirl', 'miss_cypher', 'itstryhard', 'kaywee', 'maybetall', 'anoukimorgenstern', 
		'timeoutwithbits', 'mrjakewoof', 'thatkat', 'murkedchicken', 'bowelmovement', 'theonefoster', 'robovalkia', 
		'tofulati'}

ttv_emotes = {'(ditto)', 'PepePls', 'RareParrot', 'dancepls', 'weSmart', 'gachiGASM', 'ImTriggered', 'MEGALUL', 'HYPERLUL', 
			  'WaitWhat', 'HAhaa', 'FeelsOhWait', 'EZ', 'OMEGALUL', 'GODLUL', 'COGGERS', 'POGGERS', 'PepeHands', 'HYPERS', 
			  'monkaSHAKE', 'monkaX', 'gachiBASS', 'ppOverheat', 'Clap', 'monkaGun', 'monkaHmm', 'HYPERCLAP', 'PepoDance', 
			  'sumSmash', 'AYAYA', 'Dance', 'PartyParrot', 'Pepega', 'monkaTOS', 'Monkas', 'peepoSad', 'REEEE', 'FeelsTastyMan', 
			  'peepoS', 'BLELELE', 'pepeClap', 'pepeD', 'PepeHands', 'PepeLaugh', 'keanU', 'blobDance', 'pepeJAM', 'gachiHYPER', 
			  'RainbowPls', 'McRightClick', 'imlunaSleep', 'valkHyperQ', 'reinCharge', 'valkHat'}

ffz_emotes = {"KEKW", "LULW", "POGGIES", "PepeLmao", "Pog", "PogU", "SillyChamp", "jmanLenny", "monkaW"}

valkia_emotes = {"valkLUL"}

spam_phrases = {"pls riot", "riot pls", "pls key", "drop me pls", "drop me plz", "need key", "no drop", "still no drop", "no key", "no keys",}
spam_regexs = {"k+e+y+([zs]+)?([!?]+)?", "k+e+y+ p+l+[sz]+", "(p+l+[sz]+ )?d+r+o+p+([zs]+)?[!.?]*", "d+r+o+p+([zs]+)? (p+l+[sz]+)[!.?]*", "d+r+o+p+( m+e+)?", "d+r+o+p+ k+e+y+[sz]+"}

# allowed_phrases = {"gg", "ggg", "gggg", "f", "ffs", "gj", "ggs", "hi", "hii", "sad", "gl", "hf", "glhf", "jk", "ads", "gas", "kk"}

all_emotes = ttv_emotes | ffz_emotes | valkia_emotes

non_english_chars = set("µàáâãäåæçèéêëìíîïñòóôõöỏøùúûüýćčđğşűžơưαβγδζηθικλμνξπτυχψωϕϵабвгдежзийклмнопрстуфхцчшъыьэюя־׀׆אבגדהוזחטיךכלםמןנסעףפץצקרשתװױײابتحخرسششسیشسزصضعقكلويกงดตนมยรลอะัาูเไ่้აევთლორსქấệồいぅだちㄱㄲㄳㄴㄵㄶㄷㄸㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅃㅄㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ䶬一世个了些件会何你芜湖使俄偶全其冲前勇句可啊喔喜好字實將尝常很惡懒成我捷掉擅敏敢时是来棒棕機欢比活流测激然狐狗狸生用界的真码符粹組纯臭至色茶草落要词试语赛跳車过这长门零青검국글난모세요인자좀주짐키한ｋઅંતેતો")

# Create subscribers object from disk if available:
#if path.exists("subscribers.txt"):
#	with open("subscribers.txt", "r", encoding="utf-8") as f:
#		try:
#			raw = f.read()
#			d = eval(raw)
#			subscribers = dict(d)
#		except:
#			subscribers = dict()
#else:
#	subscribers = dict()

#def get_subs():
#	global subscribers
#	while True:
#		subscribers = get_subscribers()
#		with open("subscribers.txt", "w", encoding="utf-8") as f:
#			out = str(subscribers)
#			f.write(out)
#		sleep(5*60) # update every 4 mins

#subs_thread = Thread(target=get_subs)
#subs_thread.start()

def log(s):
    """
    Takes a string, s, and logs it to a log file on disk with a timestamp. Also prints the string to console.
    """
    current_time = localtime()
    year   = str(current_time.tm_year)
    month  = str(current_time.tm_mon).zfill(2)
    day    = str(current_time.tm_mday).zfill(2)
    hour   = str(current_time.tm_hour).zfill(2)
    minute = str(current_time.tm_min).zfill(2)
    second = str(current_time.tm_sec).zfill(2)
    
    log_time = day + "/" + month + " " + hour + ":" + minute + ":" + second 

    print(s)
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(log_time + " - " + s + "\n")

def respond_message(user, message):
	lower_msg = message.lower()
	global bot

	if message[0] == "!":
		command = message[1:].split(" ")[0].lower()

		global cooldowns
		global command_last_used

		if command in cooldowns and command in command_last_used and command_last_used[command] > time() - cooldowns[command]:
			log(f"Not responding to command {command} by user {user} within cooldown time.")
			return
		else:
			command_last_used[command] = time()

		global all_emotes
		global fortunes
		global non_english_chars
		global caps_filter
		global spam_filter
		global last_drop_reply
		global last_watchtime_reply

		if command in ["dice", "roll"]:
			number = random.choice(range(1,7))
			bot.send_message(user + " rolled a dice and got a " + str(number))
			return
		elif command == "fortune":
			fortune = random.choice(fortunes)
			bot.send_message(user + ", your fortune is: " + fortune)
			log("Sent fortune in response to user {u}.".format(u=user))
			return
		#elif command == "stat":
		#	stat = message[1:].split(" ")[1]
		#	output = get_stat(stat)
		#	bot.send_message(output)
		elif False and command == "valorant":

			try:
				target = message.split(" ")[1]
			except IndexError: # no target specified
				target = user

			if target[0] == "@": # ignore @ tags
				target = target[1:]

			time_left = 1591074000 - time()
			if time_left < 0:
				bot.send_message("Valorant is now available!")
				log(f"Sent Valorant  time to {user}, targeting {target}, showing that the beta is over.")
			else:
				hours = int(time_left // 3600)
				time_left = time_left % 3600
				mins = int(time_left // 60)
				secs = int(time_left % 60)
				hs = "h" if hours == 1 else "h"
				ms = "m" if mins == 1 else "m"
				ss = "s" if secs == 1 else "s"
				
				if hours > 0:
					bot.send_message(f"/me @{target} Valorant will be released for public download in {hours}{hs}, {mins}{ms} and {secs}{ss}!")
				else:
					bot.send_message(f"/me @{target} Valorant will be released for public download in {mins}{ms} and {secs}{ss}!")

				log(f"Sent Beta end time to {user}, targeting {target}, showing {hours}{hs}, {mins}{ms} and {secs}{ss}")

			return

		elif command == "triangle" and user in mods:
			
			try:
				emote = message.split(" ")[1]
			except:
				return

			num = 3
			
			try:
				num = int(message.split(" ")[2])
			except IndexError:
				pass # no value given: leave it at 3
			except ValueError: # if conversion to int fails, e.g. int("hello")
				num = 3
			
			if emote != "":
				if num > 5:
					num = 5

				big_msg = "" # allows the two messages to be sent together instantaneously, with no delay between them. Otherwise it's possible for another user to send a message in the small time gap between messages and ruin the effect.
		
				counts = list(range(1,num+1)) + list(range(1,num)[::-1])
				for count in counts:
					big_msg += ((emote + " ") * count) + "\r\nPRIVMSG #valkia :"
					#bot.send_message((emote + " ") * count) # original implementation
				big_msg.rstrip("\r\nPRIVMSG #valkia :")
				bot.send_message(big_msg)
				log("Sent triangle of {e}, of size {s}, in response to user {u}.".format(s=num, u=user, e=emote))
				return

		elif command == "valkface" and user in mods:
			#"PRIVMSG #" + self.channel + " :" + msg + "\r\n"
			bot.send_message("valkW1 valkW2\r\nPRIVMSG #valkia : valkW3 valkW4")
			log("Sent valkface in response to user {u}.".format(u=user))
			return
		elif command == "day":
			days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
			real_day = days[date.today().weekday()]
			days.remove(real_day)
			
			day = random.choice(days)
		
			bot.send_message("Valkia thinks that today is " + day + "! valkHyperz valkOk ")
			log("Sent random day in response to user {u}.".format(u=user))
		elif command == "month":
			months = ["January", "Feburary", "March","April", "May", "June", "July", "August", "September", "October", "November", "December"]
			real_month = months[date.today().month]
			months.remove(real_month)
			
			month = random.choice(months)
		
			bot.send_message("Valkia thinks that it is " + month + "! valkHyperz valkOk ")
			log("Sent random month in response to user {u}.".format(u=user))
		elif command == "mschedule":
			bot.send_message("Monday - Thursday 12pm GMT / 7am ET")
			bot.send_message("Friday - no stream")
			bot.send_message("Saturday - Sunday 12pm GMT / 7am ET")
			log("Sent mschedule in response to user {u}.".format(u=user))
		
#		elif command == "subgoal":
#			if len(subscribers) == 0: 
#				return # subs haven't been initialised yet or there's some problem
#
#			goal = get_data("subgoal")
#
#			try:
#				int(goal)
#			except:
#				bot.send_message("No sub goal is set.")
#				log("No sub goal set, in response to user {u}.".format(u=user))
#				return
#
#			subs = len(subscribers)
#			points = -11 # two tier 3 subs, for Valkia and StreamElements, aren't counted toward points
#			tiers = {"1000":[], "2000":[], "3000":[]}
#
#			for sub in subscribers:
#				tier = subscribers[sub]["tier"]
#				if tier == "1000":
#					points += 1
#				elif tier == "2000":
#					points += 2
#				elif tier == "3000":
#					points += 6
#				tiers[tier].append(sub)
#
#			subs_remaining = goal-points
#
#			if subs_remaining < 0:
#				bot.send_message("/me The sub goal has been reached! ({s}/{g})".format(s=f'{points:,}', g=f'{goal:,}'))
#				log("Sent sub goal reached, in response to user {u}.".format(u=user))
#				return
#			else:
#				bot.send_message("/me There are only {s} subscribers left until we hit our sub goal of {goal} subscribers! Use !sub or !prime to help us get there valkFlex valkPrime".format(s=f'{subs_remaining:,}', goal=f'{goal:,}'))
#				log("Sent subgoal (goal={g}, subs left={s}) in response to user {u}.".format(u=user, s=subs_remaining, g=goal))
#				return
#		elif command == "whogifted":
#			try:
#				target = message.split(" ")[1]
#			except IndexError: # no target specified
#				target = user
#		
#			if target[0] == "@": # ignore @ tags
#				target = target[1:]
#		
#			target = target.lower()
#
#			if target in subscribers:
#				if subscribers[target]["is_gift"]:
#					try:
#						gifter = subscribers[target]["gifter_name"]
#					except KeyError:
#						return
#					bot.send_message("/me @{target}'s current subscriprion was gifted to them by @{gifter}! Thank you! valkGift valkLove".format(target=target, gifter=gifter))
#					log("Sent whogifted (target={t}, gifter={g}) in response to user {u}.".format(t=target, g=gifter, u=user))
#					return
#				else:
#					bot.send_message("/me @{target} subscribed on their own this time. Thank you! valkPrime".format(target=target))
#					log("Sent whogifted (target {t} subbed on their own) in response to user {u}.".format(u=user, t=target))
#					return
#			else:
#				bot.send_message("/me @{target} is not a subscriber.".format(target=target))
#
#		elif command == "howmanygifts":
#			try:
#				target = message.split(" ")[1]
#			except IndexError: # no target specified
#				target = user
#		
#			if target[0] == "@": # ignore @ tags
#				target = target[1:]
#		
#			target = target.lower()
#		
#			count = 0
#		
#			for sub in subscribers:
#				gifter = subscribers[sub]["gifter_name"].lower()
#				if gifter == target:
#					count+=1
#		
#			if count == 0:
#				bot.send_message("None of the current subscribers were gifted by {t}.".format(t=target))
#			else:
#				bot.send_message("/me {c} of the current subscribers were gifted by {t}! Thanks for the support <3 valkGift".format(c=count, t=target))
		elif command in {"followgoal", "followergoal"}:
			goal = get_data("followgoal")
		
			url = "https://api.twitch.tv/helix/users/follows?to_id=3481156"

			try:
				data = requests.get(url, headers=authorisation_header).json()
				followers = data["total"]
				followers_left = goal - followers
				if followers_left > 0:
					bot.send_message("/me There are only {f} followers to go until we hit our follow goal of {g}! valkHype".format(f=f'{followers_left:,}', g=f'{goal:,}'))
					log("Sent followgoal of {f}/{g} in response to {u}.".format(f=f'{followers_left:,}', g=f'{goal:,}', u=user))
				else:
					bot.send_message("/me The follower goal of {g} has been met! We now have {f} followers! valkHype".format(f=f'{followers:,}',g=f'{goal:,}'))
					log("Sent followgoal has been met {f}/{g} in response to {u}.".format(f=f'{followers:,}', g=f'{goal:,}', u=user))
			except (ValueError, KeyError) as ex:
				log("Error in followgoal command: " + ex)

		elif command == "ytsubgoal":
			try:
				yt_subs = int(get_youtube_sub_count("Valkia"))
			except ValueError as ex:
				log("Value Error when retrieving youtube subscriber count: " + str(ex))
				return
			except Exception as ex:
				log("Value Error when retrieving youtube subscriber count: " + str(ex))
				return

			goal = get_data("ytsubgoal")
			subs_remaining = goal - yt_subs
			if subs_remaining > 0 :
				bot.send_message("/me Valkia's youtube channel is only {r} subscribers away from hitting his subscriber goal of {g}!".format(r=f'{subs_remaining:,}', g=f'{goal:,}'))
				log("Sent youtube subgoal ({r}/{g}) in response to {u}.".format(r=f'{subs_remaining:,}', g=f'{goal:,}', u=user))
			else:
				bot.send_message("/me Valkia's youtube channel has passed the subscriber goal of {g}!".format(r=f'{subs_remaining:,}', g=f'{goal:,}'))
				log("Sent youtube subgoal PASSED ({r}/{g}) in response to {u}.".format(r=f'{subs_remaining:,}', g=f'{goal:,}', u=user))
				
		elif command == "msocial":
			bot.send_message("/me Twitter: www.twitter.com/officialvalkia")
			bot.send_message("/me YouTube: www.youtube.com/officialvalkia") 
			bot.send_message("/me Instagram: www.instagram.com/officialvalkia")
			log("Sent msocial in response to user {u}.".format(u=user))

		elif "unbind crouch" in lower_msg:
			bot.send_message("!unbind @" + user)
			log("Sent !unbind in response to user {u}.".format(u=user))

		if user in mods:
			if command in ["setrank", "editrank"]:
				rank = " ".join(message.split(" ")[1:])
				peak = get_data("peakrank")
				touser = "{touser}" # difficult to include this in a formatted string
				set_data("currentrank", rank)
				bot.send_message(f"!command edit rank /me ${touser} Valkia is currently ranked {rank}. He placed at Silver ll and peaked at {peak}.")
				log(f"Set rank to {rank} in response to {user}")

			if command in ["setpeak", "editpeak"]:
				rank = get_data("currentrank")
				peak = " ".join(message.split(" ")[1:])
				touser = "{touser}" # difficult to include this in a formatted string
				set_data("peakrank", peak)
				bot.send_message(f"!command edit rank /me ${touser} Valkia is currently ranked {rank}. He placed at Silver ll and peaked at {peak}.")
				log(f"Set peak to {peak} in response to {user}")

			global language_filter
			global auto_messages #can't put inside the relevant commands bc of python being dumb

			if command == "msginterval":
				try:
					interval = int(message.split(" ")[1])
				except:
					return

				if interval < 20:
					bot.send_message("@" + user + " Minimum value is 20.")
					return #don't change value

				global msg_interval
				try:
					set_data("msg_interval", interval)
				except:
					return
			
				msg_interval = interval
				bot.send_message("/me @{u} Automatic messages will now send every {s} seconds.".format(u=user, s=msg_interval))
				log("Set messageinterval to {i} in response to user {u}.".format(u=user, i=msg_interval))
				return
			elif command == "langfilter":
				if language_filter:
					language_filter = False
					set_data('language_filter', False)
					bot.send_message("/me @" + user + " language filter is now disabled.")
					log("langfilter disabled in response to user {u}.".format(u=user))
				else:
					language_filter = True
					set_data('language_filter', True)
					bot.send_message("/me @" + user + " language filter is now enabled.")
					log("langfilter enabled in response to user {u}.".format(u=user))
			elif command == "addmsg":
				new_msg = " ".join(message.split(" ")[1:])
				if new_msg not in auto_messages:
					auto_messages.append(new_msg)
					set_data('auto_messages', auto_messages)
					bot.send_message("@" + user + " Message added.")
					log("Added message {m} in response to user {u}.".format(u=user, m=new_msg[:12]+".."))
					return
				else:
					bot.send_message("@" + user + " That message already exists.")
					return

			elif command in ["delmsg", "rmvmsg", "removemsg"]:
				msg_to_delete = " ".join(message.split(" ")[1:]).lower()
				for m in auto_messages:
					if m.lower().startswith(msg_to_delete):
						auto_messages.remove(m)
						bot.send_message("@" + user + " Message deleted.")
						log("Deleted message {m} in response to user {u}.".format(u=user, m=m))
						set_data('auto_messages', auto_messages)
						return

				bot.send_message("@" + user + " Message not found.")
				return
			elif command == "capsfilter":
				if caps_filter:
					caps_filter = False
					set_data('caps_filter', False)
					bot.send_message("/me @" + user + " block caps filter is now disabled.")
					log("capsfilter disabled in response to user {u}.".format(u=user))
					return
				else:
					caps_filter = True
					set_data('caps_filter', True)
					bot.send_message("/me @" + user + " block caps filter is now enabled.")
					log("capsfilter enabled in response to user {u}.".format(u=user))
					return

			elif command == "spamfilter":
				if spam_filter:
					spam_filter = False
					set_data('spam_filter', False)
					bot.send_message("/me @" + user + " spam filter is now disabled.")
					log("spamfilter disabled in response to user {u}.".format(u=user))
					return
				else:
					spam_filter = True
					set_data('spam_filter', True)
					bot.send_message("/me @" + user + " spam filter is now enabled.")
					log("spamfilter enabled in response to user {u}.".format(u=user))
					return

			elif command == "messages":
				global enable_messages

				if enable_messages:
					set_data('enable_messages', False)
					bot.send_message("/me @" + user + " regular messages are now disabled.")
					log("Regular messages disabled in response to user {u}.".format(u=user))
				else:
					set_data('enable_messages', True)
					bot.send_message("/me @" + user + " regular messages are now enabled.")
					log("Regular messages enabled in response to user {u}.".format(u=user))

			elif False and command == "hypemode":
				mins = 5
				try:
					mins = int(message.split(" ")[1])
				except IndexError:
					pass # no value given: leave it at 5
				except ValueError: # if conversion to int fails, e.g. int("hello")
					mins = 5

				if mins > 100:
					mins = 100

				if mins < 1:
					mins = 1

				bot.send_message("/me @" + user + " Hype Mode enabled! Will not timeout anyone for the next {m} minutes.".format(m=mins))
				log("hypemode enabled for {m} mins, in response to user {u}.".format(u=user, m=mins))
				global hypemode_until
				hypemode_until = time() + (mins*60)
				return

			elif command == "dropalert":
				bot.send_message("/me @valkia ⚠️🚨ALERT STREAMER 🚨 ⚠️YOUR DROPS ARE NOT ENABLED 🎙️ valkReee valkDab ")

			elif command in ["setcolour", "setcolor"]:
				try:
					colour = message.split(" ")[1]
				except(ValueError, IndexError):
					colour = "default"

				if colour.lower() in ["default", "blue","blueviolet","cadetblue","chocolate","coral","dodgerblue","firebrick","goldenrod","green","hotpink","orangered","red","seagreen","springgreen","yellowgreen"]:
					valid = True
				else:
					valid = False

				# ONLY WORKS WITH TWITCH PRIME:
				#if colour[0] == "#": 
				#	if len(colour) == 7:
				#		for c in colour[1:].lower():
				#			if c not in "0123456789abcdef":
				#				valid = False
				#				break
				#		else:
				#			valid=True

				if valid:
					if colour == "default":
						bot.send_message("/color HotPink")
					else:
						bot.send_message("/color " + colour)
					sleep(2)
					bot.send_message("Colour updated! kaywee1AYAYA")
				else:
					bot.send_message("That colour isn't right.")

	if lower_msg in ["ayy", "ayyy", "ayyyy"]:
		bot.send_message("lmao")
		log("Sent lmao in response to user {u}.".format(u=user))
		return

	if message == "valkW1 valkW2":
		bot.send_message("Jebaited")
		log("Sent Jebaited in response to {u}.".format(u=user))

	if message == "mizkifW1 mizkifW2":
		bot.send_message("Jebaited")
		log("Sent Jebaited in response to {u}.".format(u=user))

	#elif "birthday" in lower_msg and "feelsbirthday" not in lower_msg:
	#	bot.send_message("FeelsBirthdayMan")
	#	log("Sent FeelsBirthdayMan in response to user {u}.".format(u=user))

	if user not in mods: 
		for phrase in ["retard, faggot"]:
			if phrase in lower_msg:
				bot.send_message("/timeout " + user + " 600")
				bot.send_message("@" + user + " Try a different word.")
				log(f"Timed out {user} for use of {phrase}.")
				return

#		if user not in subscribers:
#			if spam_filter:
#				if lower_msg in spam_phrases or any(re.fullmatch(r, lower_msg) for r in spam_regexs):
#					bot.send_message(f"/timeout {user} 60")
#					bot.send_message(f"!drops @{user}")
#					log(f"Timed out {user} for spam phrase: {lower_msg}")
#					return
#
#				if (len(message) == 1 
#					and lower_msg in "abcdeghijlmnopqrstuvwxyz1234567890()[];.,/#~'"):
#						bot.send_message("/timeout @" + user + " 60")
#						log("Timed out {u} for single char: {m}".format(u=user, m=lower_msg))
#						#bot.send_message("@" + user + " no need for the pointless spam.")
#						return
#
#				#if message.startswith("\x01ACTION"):
#				#	bot.send_message("/timeout " + user + " 60")
#				#	bot.send_message("/me @" + user + " - Please don't use /me here.")
#
#			if caps_filter: #capital letters check
#				words = [w for w in message.split(" ") if w not in all_emotes]
#				chars = "".join(c for c in "".join(w for w in words) if c.lower() in "abcdefghijklmnopqrstuvwxyz")
#				caps = "".join(char for char in chars if char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ") # copy only capitals
#	
#				if len(chars) > 14 and len(caps) > 0.8 * len(chars) and len(set(words)) >= 3: #set(words) makes sure it only counts unique words
#					bot.send_message(f"/timeout {user} 60")
#					bot.send_message(f"@{user} No need to shout. valkOut (No block caps please.)")
#					log("Timed out {u} for use of capitals: {m}".format(u=user, m=message))
#					return

## APPLIES TO ALL ##

		if language_filter and any(chr in lower_msg for chr in non_english_chars):
			bot.send_message("/timeout " + user + " 5")
			bot.send_message("/me @" + user + " English only in chat please. (!english)")
			log("Timed out {u} for non-english: {m}".format(u=user, m=lower_msg))
			return

		if "@robovalkia" in lower_msg:
			bot.send_message("@" + user + " I'm a bot, so I can't help you. Try talking to one of the awesome human mods instead.")
			log("Responded to @RoboValkia in response to {u}.".format(u=user, m=lower_msg))

def get_data(name):
	try:
		with open("config.txt", "r") as f:
			file = f.read()
			data = dict(eval(file))
	except FileNotFoundError as ex:
		return None
	except ValueError as ex:
		return None

	if name in data:
		return data[name]
	else:
		return None

def set_data(name, value):
	with suppress(FileNotFoundError, ValueError):
		with open("config.txt", "r") as f:
			file = f.read()
			data = dict(eval(file))
	#except FileNotFoundError as ex:
	#	return None
	#except ValueError as ex:
	#	return None

	data[name] = value

	with open("config.txt", "w") as f:
		f.write(str(data))

if __name__ == "__main__":
	#subs()
	bot = ChatBot(bot_name, password, channel_name)
	if any(c in non_english_chars for c in "abcdefghijklmnopqrstuvwxyz1234567890 |`¬,./;'#[]<>?:@~{}-=_+!\"£$%^&*()\\"):
		bot.send_message("@theonefoster initialisation error - check logs.") # double check I haven't put any obvious valid characters in the banned list.. as one slipped in once and it was bad.
		exit()

	log("Started bot.")

	last_msg = 0
	last_drop_reply = 0
	last_watchtime_reply = 0
	msg_num = 2
	msg_interval = get_data("msg_interval")
	msg_count = 0
	language_filter = get_data('language_filter')
	caps_filter = get_data('caps_filter')
	spam_filter = get_data('spam_filter')
	enable_messages = get_data('enable_messages')
	hypemode_until = 0
	cooldowns = get_data("cooldowns")
	command_last_used = dict()
	modwall = 0
	modwall_mods = set()

	auto_messages = get_data('auto_messages')

	while True:
		messages = bot.get_messages()

		if hypemode_until > time():
			sleep(hypemode_until-time())
			bot.reset_socket()
			continue

		for user, message in messages:
			if message != "" and user != "" and user != "streamelements" and user != "robovalkia":
				try:
					respond_message(user, message)
				except Exception as ex:
					log("Exception in Respond_Message - " + str(ex) + f". Message was {message} from {user}.")
				msg_count+=1
			if user in mods:
				modwall += 1
				modwall_mods.add(user)
				if modwall == 10 and len(modwall_mods) >= 3:
					bot.send_message("/me #modwall ! valkFlex")
				if modwall == 20 and len(modwall_mods) >= 3:
					bot.send_message("/me #MEGAMODWALL valkDab")
			else:
				modwall = 0
				modwall_mods = set()


		if user == "streamelements":
			continue

		sleep(0.25)

		try:
			if enable_messages and last_msg < time() - msg_interval and msg_count >= 20:
				if len(auto_messages) > 0 and auto_messages is not None:
					last_msg = time()
					msg_count = 0
					bot.send_message(auto_messages[msg_num])
					msg_num += 1
					if msg_num == len(auto_messages):
						msg_num = 0
					continue
		except Exception as ex:
			log("Exception in Auto Messages - " + str(ex))
