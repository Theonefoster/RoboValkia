from socket import socket
from time import time, sleep

class NotInitialisedException(Exception):
	def __init__(self, args):
		if args:
			self.message = args[0]
		else:
			self.message = None

class ChatBot():
	def __init__(self, username, password, channel):
		self.initialised = False
		
		self.username = username.lower()
		self.password = password
		self.channel  = channel.lower()
		
		self._open_socket()

	def _open_socket(self):
		self.socket = socket()
		self.socket.connect(("irc.twitch.tv", 6667))

		opening_request = "PASS {password}\r\nNICK {username}\r\nJOIN #{channel}\r\n".format(password=self.password, username=self.username, channel=self.channel).encode("utf-8")
		self.socket.send(opening_request)

		readbuffer = ""
		success = False

		while not success:
			next_bytes = self.socket.recv(4096).decode("utf-8")
			readbuffer += str(next_bytes)
			lines = readbuffer.split("\r\n")

			if lines == [""]:
				raise NotInitialisedException("Unable to log into Twitch: probably invalid password.")

			for line in lines:
				if "Invalid NICK" in line:
					raise NotInitialisedException("Unable to log into Twitch: invalid username.")
				print(line)
				if "End of /NAMES list" in line: # keep loading until end of names list
					success = True
					break # quits the For.. although probably at the end of lines anyway
		
		#	raise NotInitialisedException("Unable to initialise bot: unknown response from Twitch.")

		self.initialised = True

	def get_messages(self):
		"""
		Receives new messages from chat since the last call to this function, or since bot was initialised.
		Checks chat no more frequently than self.checkrate seconds.
		Each message in the list is a tuple of (username, message)
		Username is in lowercae.
		"""

		if not self.initialised:
			raise NotInitialisedException("The chatbot must be initialised before a message can be sent.")

		next_bytes = self.socket.recv(2048).decode("utf-8")

		lines = next_bytes.split("\r\n")

		while "" in lines:
			lines.remove("")

		messages = []

		for line in lines:
			if line[:4] == "PING":
				self.send_pong()
				continue

			try:
				end_of_name = line.index("!")
			except ValueError:
				continue # bad line

			try:
				name = line[1:end_of_name].lower()
				message = ":".join(line.split(":")[2:]) #everything after the third colon
			except IndexError:
				continue # bad line

			messages.append((name, message))

		return messages

	def send_message(self, msg):
		"""Send a message to the channel."""
		if not self.initialised:
			raise NotInitialisedException("The chatbot must be initialised before a message can be sent.")

		bytes_message = ("PRIVMSG #" + self.channel + " :" + msg + "\r\n").encode('utf-8')
		try:
			self.socket.send(bytes_message)
		except AttributeError:
			raise NotInitialisedException("The chatbot must be initialised before a message can be sent.")

	def send_ping(self):
		raise NotImplementedError("I'll build this later")

	def set_checkrate(self, check_rate):
		"""Check rate is the fastest rate, in seconds, the bot checks for new messages. Default is 0.5"""
		self.checkrate = check_rate

	def send_pong(self):
		msg = "PONG :tmi.twitch.tv\r\n".encode('utf-8')
		self.socket.send(msg)

	def reset_socket(self):
		"""Re-creates the socket object"""
		del self.socket
		self._open_socket()
