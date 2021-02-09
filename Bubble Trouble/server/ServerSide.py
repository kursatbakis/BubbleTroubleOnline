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
                print(content)
                if content['type'] == 'connect':
                    usernames[uniqueIdCounter] = content['name']
                    ipAddresses[uniqueIdCounter] = content['ip']
                    result = sendPacket(packets.success(uniqueIdCounter), client)
                    uniqueIdCounter += 1
                elif content['type'] == 'enqueue':
                    print('enqueue')
                    id = content['id']
                    matchablePlayers.add((Client(id, ipAddresses[id], usernames[id]), client))
                elif content['type'] == 'goodbye':
                    id = content['id']
                   # sendPacket()

        except Exception as e:
            print('Error(Tcp) ', e)

def makeBalls():
    ball1 = {
        'x': 100,
        'y': 200,
        'size': 5,
        'color': 0
    }
    ball2 = {
        'x': 500,
        'y': 200,
        'size': 5,
        'color': 1
    }
    return [ball1, ball2]

def notifyMatch(player1, cn1, player2, cn2):

    sendto2 = packets.matchFound(player1.id, player1.name, 9999)
    sendto1 = packets.matchFound(player2.id, player2.name, 9999)
    sendPacket(sendto1, cn1)
    sendPacket(sendto2, cn2)

    balls = makeBalls()
    x1 = 70
    x2 = 470
    wait = 3
    lives = 5
    packet1=packets.levelInit(r_lives=lives, wait=wait, x=x1, rivalx=x2, balls=balls)
    packet2=packets.levelInit(r_lives=lives, wait=wait, x=x2, rivalx=x1, balls=balls)
    sendPacket(packet1, cn1)
    sendPacket(packet2, cn2)

def listenByUdp():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.bind(('', 2182))
        result = select.select([s], [], [])
        while True:
            try:
                msg = result[0][0].recv(1024)
                data = json.loads(msg.decode('utf8'))
                print(data)
                if data['type'] == 'hit':
                    s.sendto(packets.hitBall(data['ball'], uniqueBallId, uniqueBallId + 1), ('<broadcast>', 2182))
                    uniqueBallId += 2
                elif data['type'] == 'update':
                    x = data['x']
                    dir = data['dir']
                    shoot = data['shoot']
                    shield = data['shield']
                    id = data['id']
                    s.sendto(packets.update(id, x, dir, shoot, shield), ('<broadcast>', 2182))
                elif data['type'] == 'dead':
                    id = data['id']
                    remaining = data['remaining']
                    s.sendto(packets.dead(id, remaining), ('<broadcast>', 2182))
            except Exception as e:
                print("Error(Udp) ", e)

def startMatchQueue():
    while True:
        if len(matchablePlayers) >= 2:
            player1, cn1 = matchablePlayers.pop()
            player2, cn2 = matchablePlayers.pop()
            notifyMatch(player1, cn1, player2, cn2)
            break


Thread(target=startMatchQueue, args=(), daemon=True).start()
Thread(target=listenByUdp, args=(), daemon=True).start()
acceptConnections()
