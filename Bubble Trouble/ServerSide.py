import json
import queue
import subprocess
import socket
import time
import packets
from threading import Thread

numberOfConnections = 0
defaultPort = 2181
uniqueIdCounter = 1
matchablePlayers = set()
usernames = {}
ipAddresses = {}

class Player:
	def __init__(self, id, ip, name):
		self.id = id
		self.ip = ip
		self.name = name

def getAvailablePort():
	return 43434

def acceptConnections():
	global numberOfConnections
	while numberOfConnections <= 100:
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			s.bind(('', defaultPort))
			print("asd")
			s.listen()
			conn, addr = s.accept()
			numberOfConnections += 1
			Thread(target = listenToClient, args = (conn,), daemon = True).start()

def sendPacket(packet, client):
	try:
		client.send(packet)
		return 0
	except BrokenPipeError as e:
		return -1
	except OSError as e:
		return -2
		
def listenToClient(client):
	while True:
		try:
			content = client.recv(1024).decode('utf8')
			if content: 
				content = json.loads(content)
				if content['type'] == 'connect':
					usernames[uniqueIdCounter] = content['name']
					ipAddresses[uniqueIdCounter] = content['ip']
					result = sendPacket(successPacket())
					print('connect', result)
				elif content['type'] == 'enqueue':
					print('enqueue')
					id = content['id']
					matchablePlayers.add(Player(id, usernames[id], ipAddresses[ip]))
				elif content['type'] == 'goodbye':
					print('goodbye')
		except Exception as e:
			print(e)
			break

def notifyMatch(player1, player2):
	print("To notify match xd")

def startMatchQueue():

	while True:
		if matchablePlayers.size >= 2:
			player1 = matchablePlayers.pop()
			player2 = matchablePlayers.pop()
			notifyMatch(player1, player2)

acceptConnections()