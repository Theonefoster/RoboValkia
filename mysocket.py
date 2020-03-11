from socket import socket
import creds.credentials as c

#code = "h3r6xvtmke797kdrskd95rdifdmu4j"
password = c.password
name     = c.bot_name
channel  = c.channel_name

def open_socket():
	s = socket()
	s.connect(("irc.twitch.tv", 6667))
	pass_bytes = ("PASS " + password + "\r\n").encode('utf-8')
	s.send(pass_bytes)
	nick_bytes = ("NICK " + name + "\r\n").encode('utf-8')
	s.send(nick_bytes)
	join_bytes = ("JOIN #" + channel + "\r\n").encode('utf-8')
	s.send(join_bytes)
	print("Socket opened.")
	return s

def join_room(s):
	readbuffer = ""
	loading = True

	while loading:
		next_bytes = s.recv(4096).decode("utf-8")
		readbuffer += str(next_bytes)
		temp = readbuffer.split("\\r\\n")

		for line in temp:
			print(line)
			loading = "End of /NAMES list" not in line #keep loading until end of names list

	print("Joined chat!")

def send_message(s, msg):
	bytes_message = ("PRIVMSG #" + channel + " :" + msg + "\r\n").encode('utf-8')
	s.send(bytes_message)
	print("Sent message: " + msg)