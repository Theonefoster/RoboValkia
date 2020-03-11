from mysocket import open_socket, join_room, send_message
from get_stat import get_stat
from time import sleep, time
from fortunes import fortunes
import random

s = open_socket()
join_room(s)

def respond_message(user, message):
	if message[0] == "!":
		command = message[1:].split(" ")[0]

		if command == "hello":
			try:
				name = message.split(" ")[1]
			except:
				return
			if name != "":
				send_message(s, "Hello, " + name + "! valkHey")
			else:
				send_message(s, "Hello, " + user + "! valkHey")
		elif command == "dice":
			number = random.choice(range(6)) + 1
			send_message(s, user + " rolled a dice and got a " + str(number))
		elif command == "new":
			send_message(s, "I'm from launcher, it's my first time in the stream")
		elif command == "fortune":
			fortune = random.choice(fortunes)
			send_message(s, user + ", your fortune is: " + fortune)
		elif command == "stat":
			stat = message[1:].split(" ")[1]
			output = get_stat(stat)
			send_message(s, output)
		#elif command == "warzone":
		#	time_left = 1583866800 - time()
		#	if time_left < 0:
		#		send_message(s, "Warzone is now availble to download! More info at https://bit.ly/2xsUSPt")
		#		return
		#	else:
		#		hours = int(time_left // 3600)
		#		time_left = time_left % 3600
		#		mins = int(time_left // 60)
		#		secs = int(time_left % 60)
		#		hs = "hour" if hours == 1 else "hours"
		#		ms = "minute" if mins == 1 else "minutes"
		#		ss = "second" if secs == 1 else "seconds"
		#		send_message(s, "/me Warzone will be available for free in {m} {ms} and {s} {ss}! More info at https://bit.ly/2xsUSPt".format(h=hours, hs=hs, m=mins, ms=ms, s=secs, ss=ss))
		#elif command == "triangle":
		#	try:
		#		emote = message.split(" ")[1]
		#	except:
		#		return
		#	
		#	num = 3
		#
		#	try:
		#		num = int(message.split(" ")[2])
		#	except IndexError:
		#		pass #leave it at 3
		#	except ValueError: #if conversion to int fails, e.g. int("hello")
		#		num = 3
		#	
		#	if emote != "":
		#		if num > 4:
		#			num = 4
		#
		#		counts = list(range(1,num+1)) + list(range(1,num)[::-1])

		#		for count in counts:
		#			send_message(s, (emote + " ") * count)
		elif command == "gamble" and user == "phillyyy":
			send_message(s, "/me phillyyy went all in and lost every single one of his valkCoin LUL")

while True:
	sleep(0.5)
	next_bytes = s.recv(2048).decode("utf-8")
	temp = next_bytes.split("\r\n")

	while "" in temp:
		temp.remove("")

	for line in temp:
		if line[:4] == "PING":
			continue
		end_of_name = line.index("!")
		name = line[1:end_of_name]
		message = ":".join(line.split(":")[2:]) #everything after the third colon

		#print(name + " said: " + message)
		respond_message(name, message)
