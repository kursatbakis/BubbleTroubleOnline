import socket
import select
from threading import Thread
import json
from window import setPlayerId, matchFound, forceEnd, levelStart, rivalDied, updateplayer2, hitball


serverIp = '192.168.1.35'
port = 2181
udpSock = None


def udpSocket():
    return udpSock


def send_tcp_packet(packet, sck):
    sck.send(packet)


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def send_udp_packet(packet, sck):
    sck.sendto(packet, (serverIp, 2182))


def send_match_request(id, sck):
    send_tcp_packet(searchForMatchPacket(id), sck)


def send_connect_packet(username, sck):
    send_tcp_packet(connectPacket(username), sck)


def listenByUdp():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        global udpSock
        udpSock = s
        result = select.select([s], [], [])
        while True:
            try:
                msg = result[0][0].recv(1024)
                data = json.loads(msg.decode('utf8'))
                if data['type'] == 'level':
                    rivallives = data['r_lives']
                    balls = data['balls']
                    noOfBalls = data['noOfBalls']
                    initialX = data['initialX']
                    r_initialX = data['r_initialX']
                    wait = data['wait']
                    levelStart(rivallives, balls, noOfBalls, initialX, r_initialX, wait)
                elif data['type'] == 'dead':
                    id = data['id']
                    remaining = data['remaining']
                    if id == playerId:
                        continue
                    rivalDied()
                elif data['type'] == 's_update':
                    id = data['id']
                    x = data['x']
                    dir = data['dir']
                    shield = data['shield']
                    shoot = data['shoot']
                    if id == playerId:
                        continue
                    updateplayer2(x, dir, shield, shoot)
                elif data['type'] == 'hitBall':
                    remove = data['remove']
                    left = data['left']
                    right = data['right']
                    hitBall(remove, left, right)
            except Exception as e:
                print('Error(udp):', e)

def listenByTcp():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('', port))
        send_connect_packet('username', s)
        try:
            while True:
                content = s.recv(1024).decode('utf-8')
                if content:
                    content = json.loads(content)
                    if 'success' in content: # basari ile servera baglandik demektir.match request atilacak
                        send_match_request(content['id'], s)
                        setPlayerId(content['id'])
                    elif content['type'] == 'match': # match bulundu oyuna basla demektir
                        matchFound(content['name'], content['withId'])
                    elif content['type'] == 'forceEnd':
                        forceEnd()
        except Exception as e:
            print('Error(tcp)', e)


####  WITH TCP ####
def searchForMatchPacket(id1):
    pack = {"id": id1, "type": "enqueue"}
    return bytes(json.dumps(pack) + '\n', 'utf8')


def connectPacket(username):
    pack = {'ip': get_ip(), 'name': username, 'type': 'connect'}
    return bytes(json.dumps(pack) + '\n', 'utf8')


def goodbyePacket(id):
    pack = {'id': id, 'type': 'goodbye'}
    return bytes(json.dumps(pack) + '\n', 'utf8')


#### WITH UDP (GAME MECHANICS) ####

def coordinatesPacket(id, gameId, x, dir, shooting, shield):
    packet = {'id': id, 'gameId': gameId, 'x': x, 'dir': dir, 'type': 'update', 'shooting': shooting, 'shield': shield}
    return bytes(json.dumps(packet) + '\n', 'utf8')


def deadPacket(id, remaining):
    packet = {'id': id, 'type': 'dead', 'remaining': remaining}
    return bytes(json.dumps(packet) + '\n', 'utf8')


def hitBallPacket(id, ballId):
    packet = {'id': id, 'ball': ballId, 'type': 'hit'}
    return bytes(json.dumps(packet) + '\n', 'utf8')



