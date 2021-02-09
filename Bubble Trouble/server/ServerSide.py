import socket
import packets
import select
from threading import Thread
import json


numberOfConnections = 0
defaultPort = 2181
uniqueIdCounter = 1
matchablePlayers = set()
usernames = {}
ipAddresses = {}
ports = {3440: 1, 3441: 1, 3442: 1, 3443: 1, 3444: 1, 3445: 1, 3446: 1}
uniqueBallId = 1

class Client:
    def __init__(self, id, ip, name):
        self.id = id
        self.ip = ip
        self.name = name


def getAvailablePort():
    for (key, value) in ports.items():
        if value == 1:
            ports[key] = 0
            return key


def acceptConnections():
    global numberOfConnections
    while numberOfConnections <= 7:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('', defaultPort))
            s.listen()
            conn, addr = s.accept()
            numberOfConnections += 1
            Thread(target=listenToClient, args=(conn,), daemon=True).start()


def sendPacket(packet, client):
    try:
        client.send(packet)
        return 0
    except BrokenPipeError as e:
        return -1
    except OSError as e:
        return -2


def listenToClient(client):
    global uniqueIdCounter
    while True:
        try:
            content = client.recv(1024).decode('utf8')
            if content:
                content = json.loads(content)
                if content['type'] == 'connect':
                    usernames[uniqueIdCounter] = content['name']
                    ipAddresses[uniqueIdCounter] = content['ip']
                    result = sendPacket(packets.success(uniqueIdCounter), client)
                    uniqueIdCounter += 1
                    print('connect', result)
                elif content['type'] == 'enqueue':
                    print('enqueue')
                    id = content['id']
                    matchablePlayers.add((Client(id, ipAddresses[id], usernames[id]), client))
                elif content['type'] == 'goodbye':
                    print('goodbye')
        except Exception as e:
            print('Error:', e)


def notifyMatch(player1, cn1, player2, cn2):
    sendto2 = packets.matchFound(player1.id, player1.name, 9999)
    sendto1 = packets.matchFound(player2.id, player2.name, 9999)
    sendPacket(sendto1, cn1)
    sendPacket(sendto2, cn2)

def listenByUdp():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(('', 2182))
        result = select.select([s], [], [])
        while True:
            msg = result[0][0].recv(1024)
            data = json.loads(msg.decode('utf8'))
            print(data)
            if data['type'] == 'hit':
                pass
                #send new ball id's and removed ball id to both
            elif data['type'] == 'update':
                pass
                #send this to other client
            elif data['type'] == 'dead':
                pass
                #send to other client

def startMatchQueue():
    while True:
        if len(matchablePlayers) >= 2:
            player1, cn1 = matchablePlayers.pop()
            player2, cn2 = matchablePlayers.pop()
            notifyMatch(player1, cn1, player2, cn2)


Thread(target=startMatchQueue, args=(), daemon=True).start()
Thread(target=listenByUdp, args=(), daemon=True).start()
acceptConnections()
