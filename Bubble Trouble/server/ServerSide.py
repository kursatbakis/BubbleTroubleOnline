import socket
import packets
from threading import Thread
import json


numberOfConnections = 0
defaultPort = 2181
uniqueIdCounter = 1
matchablePlayers = set()
usernames = {}
ipAddresses = {}
ports = {3440: 1, 3441: 1, 3442: 1, 3443: 1, 3444: 1, 3445: 1, 3446: 1}


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
                    matchablePlayers.add([Client(id, ipAddresses[id], usernames[id]), client])
                elif content['type'] == 'goodbye':
                    print('goodbye')
        except Exception as e:
            print(e)
            break


def notifyMatch(player1, player2):
    sendto2 = packets.matchFound(player1[0].id, player1[0].name)
    sendto1 = packets.matchFound(player2[0].id, player2[0].name)
    sendPacket(sendto1, player1[1])
    sendPacket(sendto2, player2[1])


def startMatchQueue():
    while True:
        if len(matchablePlayers) >= 2:
            player1 = matchablePlayers.pop()
            player2 = matchablePlayers.pop()
            notifyMatch(player1, player2)


Thread(target=startMatchQueue, args=(), daemon=True).start()
acceptConnections()
